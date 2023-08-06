from crownstone_core.util.fletcher import fletcher32_uint8Arr
import math

class Microapp(object):
    def __init__(self, buf, chunk_size, app_id, protocol):
        self.buffer = buf
        self.size = len(buf)
        self.app_id = app_id
        self.protocol = protocol
        self.chunk_size = chunk_size

class MicroappPacket(object):
    def __init__(self, protocol, app_id, index, count, size, checksum, buf):
        self.protocol = protocol
        self.app_id = app_id
        self.index = index
        self.count = count
        self.size = size
        self.checksum = checksum
        self.buffer = buf

class MicroappMetaPacket(object):
    def __init__(self, protocol, app_id, opcode, param0, param1, buf):
        self.protocol = protocol
        self.app_id = app_id
        self.trigger = 0xFF
        self.opcode = opcode
        self.param0 = param0
        self.param1 = param1
        self.buffer = buf


class MicroappPacketInternal(object):

    def __init__(self, data):
        self.index = 0
        self.count = math.ceil(data.size / data.chunk_size)
        self.checksum = 0xCAFE
        self.chunk = bytearray(data.chunk_size)
        self.data = data

        self.chunk[0 : data.chunk_size] = data.buffer[0 : data.chunk_size]

    def update(self):
        # if next is available, go to next index
        if (not self.nextAvailable()):
            return
        self.index += 1
        offset = self.index * self.data.chunk_size
        if (not self.last()):
            self.chunk[0 : self.data.chunk_size] = self.data.buffer[offset : offset + self.data.chunk_size]
        else:
            print("LOG: last piece")
            # Divide into remaining parts [data 0xFF]
            remaining0 = self.data.size - offset
            remaining1 = self.data.chunk_size - remaining0
            fill_buffer = bytearray([0xFF] * remaining1)
            self.chunk[0 : remaining0] = self.data.buffer[offset : offset + remaining0]
            self.chunk[remaining0 : self.data.chunk_size] = fill_buffer[0 : remaining1]
        print("LOG: size chunk is ", len(self.chunk))

    def last(self):
        offset = self.index * self.data.chunk_size
        if self.data.size > (offset + self.data.chunk_size):
            return False
        return True

    def nextAvailable(self):
        if ((self.index + 1) < self.count):
            return True
        return False

    def getPacket(self):
        self.calculateChecksum()
        packet = MicroappPacket(self.data.protocol, self.data.app_id, self.index, self.count, self.data.size,
                self.checksum, self.chunk)
        return packet

    def calculateChecksum(self):
        if self.last():
            buf = bytearray(len(self.data.buffer))
            buf[0:len(self.data.buffer)] = self.data.buffer[0:len(self.data.buffer)]
            if len(buf) % 2 != 0:
                buf.append(0)
            self.checksum = fletcher32_uint8Arr(buf)
        else:
            # No padded by zero needed, it is already of even size
            self.checksum = fletcher32_uint8Arr(self.chunk)
        print("LOG: checksum used: ", hex(self.checksum & 0xFFFF))

    def getMetaPacket(self, offset):
        empty_buffer = bytearray([0x00] * self.data.chunk_size)
        enable = 0x01
        packet = MicroappMetaPacket(self.data.protocol, self.data.app_id, enable, offset, 0x00, empty_buffer)
        return packet

