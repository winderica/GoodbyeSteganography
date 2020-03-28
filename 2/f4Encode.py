from jpegEncode import encode
from analyze import histogramAnalyze

# writer of F4
def writeDCT(dct, index, data):
    value = dct[index]
    if value == 0:
        return False
    if (value == 1 and data == 0) or (value == -1 and data == 1):
        dct[index] = 0
        return False
    lsb = value % 2
    if value > 0 and lsb != data:
        dct[index] -= 1
    if value < 0 and lsb == data:
        dct[index] += 1
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_f4.jpg", f.read(), writeDCT), "./results/f4.png")
