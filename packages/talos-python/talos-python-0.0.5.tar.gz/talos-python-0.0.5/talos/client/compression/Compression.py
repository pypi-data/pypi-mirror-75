# -*- coding:utf-8 -*-
#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 


from talos.thrift.message.ttypes import MessageCompressionType
from talos.thrift.message.ttypes import MessageBlock
from talos.thrift.message.ttypes import MessageAndOffset
from talos.client.serialization.MessageSerializationFactory import MessageSerializationFactory
from talos.utils.Utils import current_time_mills
from talos.client.serialization.MessageSerialization import MessageSerialization
from talos.client.Constants import Constants
from io import BytesIO
import struct
import snappy
import gzip
import logging
import platform
import six
import traceback

_XERIAL_V1_HEADER = (-126, b'S', b'N', b'A', b'P', b'P', b'Y', 0, 1, 1)
_XERIAL_V1_FORMAT = 'bccccccBii'

PYPY = bool(platform.python_implementation() == 'PyPy')


class Compression(object):

    logger = logging.getLogger("Compression")

    def compress(self, msgList=None, compressionType=None):
        return self.do_compress(msgList, compressionType, MessageSerializationFactory().get_default_message_version())

    def do_compress(self, msgList=None, compressionType=None, messageVersion=None):
        messageBlock = MessageBlock(startMessageOffset=0, messageNumber=0,
                                    messageBlockSize=0, appendTimestamp=0,
                                    createTimestamp=0, transactionId=0)
        messageCompressionType = MessageCompressionType._NAMES_TO_VALUES[compressionType]
        messageBlock.compressionType = messageCompressionType
        messageBlock.messageNumber = int(len(msgList))

        createTime = current_time_mills()
        if len(msgList) > 0:
            createTime = msgList[0].createTimestamp

        try:
            # assume the message bytes size is 256KB
            messageBlockData = bytearray()
            messageSerializedBuffer = bytearray()
            dataOutputIo = BytesIO(messageSerializedBuffer)
            index = 0
            for message in msgList:
                MessageSerialization().serialize_message(message, dataOutputIo, messageVersion)
                createTime += (message.createTimestamp - createTime) / (index + 1)
            messageBlock.createTimestamp = int(createTime)

            if messageCompressionType == MessageCompressionType.NONE:
                messageBlockData = dataOutputIo.getvalue()
            elif messageCompressionType == MessageCompressionType.GZIP:
                messageBlockData = self.gzip_compress(dataOutputIo.getvalue())
            elif messageCompressionType == MessageCompressionType.SNAPPY:
                messageBlockData = self.snappy_encode(dataOutputIo.getvalue())
            else:
                raise RuntimeError("Unsupported Compression Type: " + str(compressionType))

            # close dataOutputIo
            dataOutputIo.close()

            if len(messageBlockData) > Constants.TALOS_MESSAGE_BLOCK_BYTES_MAXIMAL:
                raise ValueError("MessageBlock must be less than or equal to " +
                                 Constants.TALOS_MESSAGE_BLOCK_BYTES_MAXIMAL +
                                 " bytes, got bytes: " + len(messageBlockData))
            messageBlock.messageBlock = messageBlockData
            messageBlock.messageBlockSize = len(messageBlockData)
        except (RuntimeError, Exception) as e:
            self.logger.info("compress MessageList failed!" + str(traceback.format_exc()))
            raise e

        return messageBlock

    def decompress(self, msgBlockList=None, unHandledMessageNumber=None):
        if len(msgBlockList) > 0:
            messageAndOffsetList = []
            unHandledNumber = unHandledMessageNumber
            for messageBlock in reversed(msgBlockList):
                msgAndOffsetList = self.do_decompress(messageBlock, unHandledNumber)
                unHandledNumber += len(msgAndOffsetList)
                messageAndOffsetList[0:0] = msgAndOffsetList
            return messageAndOffsetList
        else:
            return []

    def do_decompress(self, messageBlock=None, unHandledNumber=None):
        messageBlockData = BytesIO()
        if messageBlock.compressionType == MessageCompressionType.NONE:
            messageBlockData = BytesIO(messageBlock.messageBlock)
        elif messageBlock.compressionType == MessageCompressionType.GZIP:
            messageBlockData = BytesIO(self.gzip_uncompress(messageBlock.messageBlock))
        elif messageBlock.compressionType == MessageCompressionType.SNAPPY:
            messageBlockData = BytesIO(self.snappy_decode(messageBlock.messageBlock))

        messageNumber = messageBlock.messageNumber

        messageAndOffsetList = []
        try:
            i = 0
            while i < messageNumber:
                messageAndOffset = MessageAndOffset()
                messageAndOffset.messageOffset = messageBlock.startMessageOffset + i
                message = MessageSerialization().deserialize_message(messageBlockData)
                if messageBlock.appendTimestamp:
                    message.appendTimestamp = messageBlock.appendTimestamp
                messageAndOffset.message = message
                messageAndOffset.unHandledMessageNumber = unHandledNumber + messageNumber - 1 - i

                # add message to messageList
                messageAndOffsetList.append(messageAndOffset)
                i += 1
        except Exception as e:
            self.logger.error("Decompress messageBlock failed" + str(traceback.format_exc()))
        return messageAndOffsetList

    def gzip_compress(self, c_data):
        buf = BytesIO()
        try:
            with gzip.GzipFile(mode='wb', fileobj=buf) as f:
                f.write(c_data)
            return buf.getvalue()
        except Exception as e:
            self.logger.error("compress wrong" + str(traceback.format_exc()))
        finally:
            f.close()

    def gzip_uncompress(self, c_data):
        try:
            buf = BytesIO(c_data)
            with gzip.GzipFile(mode='rb', fileobj=buf) as f:
                return f.read()
        except Exception as e:
            self.logger.error("uncompress wrong" + str(traceback.format_exc()))
        finally:
            f.close()

    def snappy_encode(self, payload, xerial_compatible=True, xerial_blocksize=32 * 1024):
        """Encodes the given data with snappy compression.

        If xerial_compatible is set then the stream is encoded in a fashion
        compatible with the xerial snappy library.

        The block size (xerial_blocksize) controls how frequent the blocking occurs
        32k is the default in the xerial library.

        The format winds up being:


            +-------------+------------+--------------+------------+--------------+
            |   Header    | Block1 len | Block1 data  | Blockn len | Blockn data  |
            +-------------+------------+--------------+------------+--------------+
            |  16 bytes   |  BE int32  | snappy bytes |  BE int32  | snappy bytes |
            +-------------+------------+--------------+------------+--------------+


        It is important to note that the blocksize is the amount of uncompressed
        data presented to snappy at each block, whereas the blocklen is the number
        of bytes that will be present in the stream; so the length will always be
        <= blocksize.

        """

        if not xerial_compatible:
            return snappy.compress(payload)

        out = BytesIO()
        for fmt, dat in zip(_XERIAL_V1_FORMAT, _XERIAL_V1_HEADER):
            out.write(struct.pack('!' + fmt, dat))

        # Chunk through buffers to avoid creating intermediate slice copies
        if PYPY:
            # on pypy, snappy.compress() on a sliced buffer consumes the entire
            # buffer... likely a python-snappy bug, so just use a slice copy
            chunker = lambda payload, i, size: payload[i:size + i]

        elif six.PY2:
            # Sliced buffer avoids additional copies
            # pylint: disable-msg=undefined-variable
            chunker = lambda payload, i, size: buffer(payload, i, size)
        else:
            # snappy.compress does not like raw memoryviews, so we have to convert
            # tobytes, which is a copy... oh well. it's the thought that counts.
            # pylint: disable-msg=undefined-variable
            chunker = lambda payload, i, size: memoryview(payload)[i:size + i].tobytes()

        for chunk in (chunker(payload, i, xerial_blocksize)
                      for i in range(0, len(payload), xerial_blocksize)):
            block = snappy.compress(chunk)
            block_size = len(block)
            out.write(struct.pack('!i', block_size))
            out.write(block)

        return out.getvalue()

    def _detect_xerial_stream(self, payload):
        """Detects if the data given might have been encoded with the blocking mode
            of the xerial snappy library.

            This mode writes a magic header of the format:
                +--------+--------------+------------+---------+--------+
                | Marker | Magic String | Null / Pad | Version | Compat |
                +--------+--------------+------------+---------+--------+
                |  byte  |   c-string   |    byte    |  int32  | int32  |
                +--------+--------------+------------+---------+--------+
                |  -126  |   'SNAPPY'   |     \0     |         |        |
                +--------+--------------+------------+---------+--------+

            The pad appears to be to ensure that SNAPPY is a valid cstring
            The version is the version of this format as written by xerial,
            in the wild this is currently 1 as such we only support v1.

            Compat is there to claim the miniumum supported version that
            can read a xerial block stream, presently in the wild this is
            1.
        """

        if len(payload) > 16:
            header = struct.unpack('!' + _XERIAL_V1_FORMAT, bytes(payload)[:16])
            return header == _XERIAL_V1_HEADER
        return False

    def snappy_decode(self, payload):

        if self._detect_xerial_stream(payload):
            # TODO ? Should become a fileobj ?
            out = BytesIO()
            byt = payload[16:]
            length = len(byt)
            cursor = 0

            while cursor < length:
                block_size = struct.unpack_from('!i', byt[cursor:])[0]
                # Skip the block size
                cursor += 4
                end = cursor + block_size
                out.write(snappy.decompress(byt[cursor:end]))
                cursor = end

            out.seek(0)
            return out.read()
        else:
            return snappy.decompress(payload)

