from PIL import Image
from matplotlib import pyplot as plt


def analyze(img, hasOffset=False):
    width, height = img.size
    pixels = [[img.getpixel((i, j)) for i in range(width)]
              for j in range(height)]
    frequency = [[0, 0] for _ in range(128)]

    for row in pixels:
        for x in row:
            frequency[x // 2][x % 2] += 1

    offset = 15 if hasOffset else 0
    plt.bar([i * 40 + offset for i in range(128)],
            list(map(lambda x: x[0], frequency)),
            width=5,
            align='center')
    plt.bar([i * 40 + 5 + offset for i in range(128)],
            list(map(lambda x: x[1], frequency)),
            width=5,
            align='center')


plt.figure(figsize=(40, 5), dpi=300)
plt.xticks([])
analyze(Image.open("./samples/lena.bmp").convert("L"))
analyze(Image.open("./samples/lena2.bmp").convert("L"), True)
plt.savefig("./results/chart.png")
