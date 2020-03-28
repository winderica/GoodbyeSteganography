from jpegEncode import encode
from analyze import histogramAnalyze

# writer of JSteg
def writeDCT(dct, index, data):
    value = dct[index]
    if value in (-1, 1, 0):
        return False
    lsb = value % 2
    if value > 0:
        dct[index] += data - lsb
    else:
        dct[index] -= data - lsb
    return True


with open("./samples/plain.txt", "rb") as f: # encode and analyze
    histogramAnalyze(encode("./samples/lena.jpg", "./samples/lena_jsteg.jpg", f.read(), writeDCT), "./results/jsteg.png")
