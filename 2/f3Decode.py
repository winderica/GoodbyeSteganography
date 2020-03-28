from jpegDecode import decode

# reader of F3
def readDCT(dct, index):
    value = dct[index]
    if value != 0:
        return value % 2
    return None


with open("./samples/plain_extracted_f3.txt", "wb") as f: # decode and save
    f.write(decode("./samples/lena_f3.jpg", readDCT))
