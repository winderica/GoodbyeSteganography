from PIL import Image

img = Image.open("./samples/lena.bmp").convert("L")  # open image
width, height = img.size  # get size
pixels = [
    [img.getpixel((i, j)) for i in range(width)]
    for j in range(height)
]  # read pixels into 2D list

with open('./samples/plain.txt', 'rb') as f:  # open plaintext file
    plaintext = f.read()  # read plaintext from plaintext file

bits = ''.join(
    '{:08b}'.format(x)
    for x in plaintext
)  # convert plaintext into bits

for i, row in enumerate(pixels):  # enumerate rows
    for j, x in enumerate(row):  # enumerate pixels
        if i * 512 + j < len(bits):  # whether index of pixel exceeds length of bits
            # set LSB of pixel
            img.putpixel((j, i), (x - x % 2 + int(bits[i * 512 + j]),))

img.save("./samples/lena2.bmp") # save image
