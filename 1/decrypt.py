from PIL import Image
import os

img = Image.open("./samples/lena2.bmp").convert("L")
width, height = img.size
pixels = [[img.getpixel((i, j)) for i in range(width)] for j in range(height)]

length = os.path.getsize('./samples/plain.txt') * 8
bits = ''

for i, row in enumerate(pixels):
    for j, x in enumerate(row):
        if i * 512 + j < length:
            bits += str(x % 2)

with open('./samples/plain2.txt', 'wb') as f:
    f.write(bytes([int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]))
