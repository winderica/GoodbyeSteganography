from PIL import Image
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd


def getFrequency(src):
    img = Image.open(src)  # open image
    width, height = img.size  # get size
    pixels = [
        [img.getpixel((i, j)) for i in range(width)]
        for j in range(height)
    ]  # read pixels into 2D list
    frequency = [[0, 0] for _ in range(128)]  # init frequency list
    for row in pixels:  # enumerate rows
        for x in row:  # enumerate pixels
            frequency[x // 2][x % 2] += 1  # update frequency
    return frequency  # return frequency list


def histogramAnalyze(srcBefore, srcAfter, dst):
    # get frequency before concealing
    frequencyBefore = getFrequency(srcBefore)
    # get frequency after concealing
    frequencyAfter = getFrequency(srcAfter)

    plt.close('all')  # close opened graphs
    plt.figure(dpi=300)  # set dpi
    df = pd.DataFrame(
        [x + y for x, y in zip(frequencyBefore, frequencyAfter)],
        index=list(range(128)),
        columns=["before:0", "before:1", "after: 0", "after: 1"]
    )  # set data
    ax = df.plot.bar(figsize=(40, 5))  # generate a histogram
    ax.set_xlabel('First 7 bits of gray scale')  # set x axis label
    ax.set_ylabel('Frequency')  # set y axis label
    plt.savefig(dst)  # save histogram


def chiSquareAnalyze(src, dst):
    img = Image.open(src)  # open image
    pixels = img.load()  # read pixels
    width, height = img.size  # get size
    chunk = 1024  # chunk size
    results = []  # result list
    for size in range(chunk, height * width, chunk):  # enumerate message size
        frequency = [0] * 256  # init frequency list
        for x in range(width):  # enumerate columns
            for y in range(size // width):  # enumerate rows
                frequency[pixels[x, y]] += 1  # update frequency

        observed = []  # observed frequencies
        expected = []  # expected frequencies
        for i in range(0, 255, 2):  # enumerate pairs
            curr = frequency[i]  # current value
            avg = (curr + frequency[i + 1]) / 2  # average value of pairs
            if curr > 0 and avg > 0:  # push only if larger than 0
                observed.append(curr)  # push into observed frequencies
                expected.append(avg)  # push into expected frequencies

        # calculate chisquare and p-value, then push into results
        results.append(stats.chisquare(observed, expected))

    plt.close('all')  # close opened graphs
    plt.figure(dpi=300)  # set dpi
    df = pd.DataFrame(
        results,
        index=list(range(chunk, height * width, chunk)),
        columns=["ChiSquare", "P"]
    )  # set data
    ax = df.plot(figsize=(25, 5), secondary_y=['P'])  # generate a plot chart
    ax.set_xlabel('Size')  # set x axis label
    ax.set_ylabel('ChiSquare')  # set y axis label
    ax.right_ax.set_ylabel('P')  # set another y axis label
    plt.savefig(dst)  # save plot chart


# perform histogram analysis
histogramAnalyze(
    "./samples/lena.bmp",
    "./samples/lena2.bmp",
    "./results/histogram.png"
)

# perform chisquare analysis
chiSquareAnalyze("./samples/lena.bmp", "./results/chiSquare1.png")
chiSquareAnalyze("./samples/lena2.bmp", "./results/chiSquare2.png")
