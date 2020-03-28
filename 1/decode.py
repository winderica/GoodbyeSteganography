from PIL import Image
import os

img = Image.open("./samples/lena2.bmp").convert("L")  # open image
width, height = img.size  # get size
pixels = [
    [img.getpixel((i, j)) for i in range(width)]
    for j in range(height)
]  # read pixels into 2D list

# get size of message(in bits)
length = 8 * os.path.getsize('./samples/plain.txt')
bits = ''  # init bits

for i, row in enumerate(pixels):  # enumerate rows
    for j, x in enumerate(row):  # enumerate pixels
        if i * 512 + j < length:  # whether index of pixel exceeds length of bits
            bits += str(x % 2)  # push LSB

with open('./samples/plain2.txt', 'wb') as f:  # open extracted plaintext file
    # write extracted plaintext
    f.write(bytes([int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]))
