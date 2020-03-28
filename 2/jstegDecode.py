from jpegDecode import decode

# reader of JSteg
def readDCT(dct, index):
    value = dct[index]
    if value in (-1, 1, 0):
        return None
    return value % 2


with open("./samples/plain_extracted_jsteg.txt", "wb") as f: # decode and save
    f.write(decode("./samples/lena_jsteg.jpg", readDCT))
