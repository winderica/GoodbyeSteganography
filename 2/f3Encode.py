from jpegEncode import encode
from analyze import histogramAnalyze

# writer of F3
def writeDCT(dct, index, data):
    value = dct[index]
    if value == 0:
        return False
    if value in (-1, 1) and data == 0:
        dct[index] = 0
        return False

    lsb = value % 2

    if lsb != data:
        if value > 0:
            dct[index] -= 1
        else:
            dct[index] += 1
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_f3.jpg", f.read(), writeDCT), "./results/f3.png")

