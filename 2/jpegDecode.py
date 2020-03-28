import numpy as np
from bitstream import BitStream
from huffman import huffmanDecode
from struct import unpack
from consts import *
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

def read(dct, stream, reader):
    index = 1
    while index < 64:
        data = reader(dct, index)
        while data is None:
            index += 1
            if index >= 64:
                return
            data = reader(dct, index)
        stream.write(int(data), bool)
        index += 1


def decode(src, reader):
    with open(src, "rb") as f:
        data = f.read()
    assert data[0x00:0x02] == SOI, "SOI not recognized"
    assert data[0x02:0x14] == APP0, "APP 0 not recognized"
    assert data[0x14:0x59] == DQT0, "DQT 0 not recognized"
    assert data[0x59:0x9e] == DQT1, "DQT 1 not recognized"
    assert data[0x9e:0xa3] == SOF0_PREFIX, "SOF 0 not recognized"
    height, = unpack('>H', data[0xa3:0xa5])
    width, = unpack('>H', data[0xa5:0xa7])
    assert data[0xa7:0xb1] == SOF0_SUFFIX, "SOF 0 not recognized"
    assert data[0xb1:0x255] == DHT, "DHT not recognized"
    assert data[0x255:0x263] == SOS, "SOS not recognized"
    assert data[-2:] == EOI, "EOI not recognized"
    stream = BitStream()
    i = 0x263
    while i < len(data) - 2:
        value = data[i:i + 1]
        stream.write(value, bytes)
        i += 1 if data[i] != 0xff else 2

    bits = BitStream()
    for yAC, _, _ in huffmanDecode(stream, height // 8 * width // 8):
        read(np.array(yAC)[zigzagReverseOrder], bits, reader)
    length = unpack('>I', bits.read(bytes, 4))[0]
    if length > len(bits) / 8:
        print("{} of {} bytes are revealed.".format(len(bits) / 8, length))
        length = len(bits) / 8
    return bits.read(bytes, length)
