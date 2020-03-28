from jpegDecode import decode

# reader of F4
def readDCT(dct, index):
    value = dct[index]
    if value > 0:
        return value % 2
    if value < 0:
        return (value + 1) % 2
    return None


with open("./samples/plain_extracted_f4.txt", "wb") as f: # decode and save
    f.write(decode("./samples/lena_f4.jpg", readDCT))
