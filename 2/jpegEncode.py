from PIL import Image
import numpy as np
from bitstream import BitStream
import cv2
from struct import pack
from consts import *
from huffman import huffmanEncode


remain = -1


def write(dct, info, writer):
    global remain
    index = 1
    while len(info) and index < 64:
        if remain != -1:
            bit = remain
            remain = -1
        else:
            bit = info.read(bool, 1)[0]
        while True:
            written = writer(dct, index, bit)
            if written:
                break
            index += 1
            if index == 64:
                remain = bit
                break
        index += 1


def toBlocks(arr, rows, columns):
    h, w = arr.shape
    assert h % rows == 0, "height is not divisble by {}".format(rows)
    assert w % columns == 0, "width is not divisble by {}".format(columns)
    return arr.reshape(h // rows, rows, -1, columns).swapaxes(1, 2).reshape(-1, rows, columns)


def updateFrequency(dct, frequency):
    for value in dct:
        if -16 <= value <= 16:
            if value not in frequency:
                frequency[value] = 1
            else:
                frequency[value] += 1


def encode(src, dst, message, writer):
    plain = pack('>I', len(message)) + message # message is left-padded by it's length
    bits = BitStream()
    bits.write( # convert message to bitstream
        np.unpackbits(np.frombuffer(plain, dtype=np.uint8)).reshape(len(plain), 8).flatten(),
        bool
    )

    with Image.open(src).convert("YCbCr") as f:
        w, h = f.size # get width and height
        y, u, v = f.split() # get Y, U and V

    # split Y, U and V into blocks of 8*8 matrix
    y = toBlocks(np.array(y, dtype=np.double) - 128, 8, 8)
    u = toBlocks(np.array(u, dtype=np.double) - 128, 8, 8)
    v = toBlocks(np.array(v, dtype=np.double) - 128, 8, 8)

    prevYDC = prevUDC = prevVDC = 0
    frequencyBefore = {}
    frequencyAfter = {}

    stream = BitStream()

    for yBlock, uBlock, vBlock in zip(y, u, v):
        # Y should be quantized
        yDCT = np.divide(cv2.dct(yBlock).flatten(), quantizationTable).round().astype(np.int)
        updateFrequency(yDCT, frequencyBefore) # update `frequencyBefore`
        write(yDCT, bits, writer) # write message bits to DCT
        updateFrequency(yDCT, frequencyAfter) # update `frequencyAfter`
        # U and V are not necessary to be quantized because all of them are formed with 0s
        uDCT = cv2.dct(uBlock).flatten().round().astype(np.int)
        vDCT = cv2.dct(vBlock).flatten().round().astype(np.int)

        # zigzag
        yAC = yDCT[zigzagOrder]
        uAC = uDCT[zigzagOrder]
        vAC = vDCT[zigzagOrder]

        # huffman encode
        huffmanEncode(stream, yAC[0] - prevYDC, yAC[1:], True)
        huffmanEncode(stream, uAC[0] - prevUDC, uAC[1:], False)
        huffmanEncode(stream, vAC[0] - prevVDC, vAC[1:], False)

        # store as previous DC value
        prevYDC = yAC[0]
        prevUDC = uAC[0]
        prevVDC = vAC[0]

    # pad by 1
    stream.write(np.ones(8 - len(stream) % 8), bool)

    with open(dst, "wb+") as f:
        # write metadata
        f.write(SOI + APP0 + DQT0 + DQT1 + SOF0_PREFIX + pack(">H", h) + pack(">H", w) + SOF0_SUFFIX + DHT + SOS)
        
        # write image data
        for i in stream.read(bytes):
            f.write(pack("B", i))
            if i == 0xff:
                f.write(pack("B", 0))

        # write EOI
        f.write(EOI)

    return frequencyBefore, frequencyAfter
