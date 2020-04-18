import numpy as np
import cv2
from utils import *


def encrypt(input, output, block_size, key):
    original_image = cv2.cvtColor(pad_image(block_size, cv2.imread(input)), cv2.COLOR_RGB2YCrCb)

    h, w, _ = original_image.shape
    w *= 3
    rows, columns = h // block_size, w // block_size

    flatten_image = to_blocks(np.transpose(original_image, (0, 2, 1)).reshape((h, w)), block_size, block_size)
    result = to_blocks(np.zeros((h, w), dtype=np.uint8), block_size, block_size)

    keys1, keys2, keys3, keys4 = key_gen(key, rows * columns)
    # Encryption
    for i, k1, k2, k3, k4 in zip(range(rows * columns), keys1, keys2, keys3, keys4):
        # Block Scrambling
        res = flatten_image[k1]
        # Block Rotation
        res = np.rot90(res, k2)
        # Block Inversion
        if k3 % 2:
            res = np.flipud(res)  # Vertical
        if k3 >= 2:
            res = np.fliplr(res)  # Horizontal
        # Negative-Positive Transformation
        if k4:
            res ^= 255

        result[i] = res

    cv2.imwrite(output, from_blocks(result, h, w))
