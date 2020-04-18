import numpy as np
import cv2
from utils import *


def decrypt(input, output, block_size, key):
    result = cv2.imread(input, cv2.IMREAD_GRAYSCALE)

    h, w = result.shape
    rows, columns = h // block_size, w // block_size

    result = to_blocks(result, block_size, block_size)
    flatten_image = to_blocks(np.zeros((h, w), dtype=np.uint8), block_size, block_size)

    keys1, keys2, keys3, keys4 = key_gen(key, rows * columns)
    # Decryption
    for res, k1, k2, k3, k4 in zip(result, keys1, keys2, keys3, keys4):
        # Inverse Negative-Positive Transformation
        if k4:
            res ^= 255
        # Inverse Block Inversion
        if k3 % 2:
            res = np.flipud(res)  # Vertical
        if k3 >= 2:
            res = np.fliplr(res)  # Horizontal
        # Inverse Block Rotation
        res = np.rot90(res, 4 - k2)
        # Inverse Block Scrambling
        flatten_image[k1] = res

    original_image = from_blocks(flatten_image, h, w).reshape((h, 3, w // 3)).transpose((0, 2, 1))

    cv2.imwrite(output, cv2.cvtColor(original_image, cv2.COLOR_YCrCb2RGB))
