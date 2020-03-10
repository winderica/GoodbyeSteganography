from PIL import Image

img = Image.open("./samples/lena.bmp").convert("L")
width, height = img.size
pixels = [[img.getpixel((i, j)) for i in range(width)] for j in range(height)]

with open('./samples/plain.txt', 'rb') as f:
    plaintext = f.read()

bits = ''.join('{:08b}'.format(x) for x in plaintext)

for i, row in enumerate(pixels):
    for j, x in enumerate(row):
        if i * 512 + j >= len(bits):
            img.putpixel((j, i), (x,))
        else:
            value = x - x % 2 + int(bits[i * 512 + j])
            img.putpixel((j, i), (value,))

img.save("./samples/lena2.bmp")
