import cv2
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def histogramAnalyze(frequency, dst):
    before, after = frequency
    plt.close('all')  # close opened graphs
    plt.figure(dpi=300)  # set dpi
    y1 = np.array(list(before.values()))[np.argsort(list(before.keys()))] # sort by keys of `before`
    y2 = np.array(list(after.values()))[np.argsort(list(after.keys()))] # sort by keys of `after`

    df = pd.DataFrame(
        zip(y1, y2),
        index=range(-16, 17),
        columns=["before", "after"]
    )  # set data
    ax = df.plot.bar(figsize=(40, 40))  # generate a histogram
    ax.set_xlabel('DCT coefficient')  # set x axis label
    ax.set_ylabel('Frequency')  # set y axis label
    plt.savefig(dst)  # save histogram
