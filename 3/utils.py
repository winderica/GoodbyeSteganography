import numpy as np
import hashlib
import math


def pad_image(size, image):
    ceil = lambda n, s: math.ceil(n / s) * s
    h, w, _ = image.shape
    padded_img = np.zeros((ceil(h, size), ceil(w, size), 3), dtype=np.uint8)
    padded_img[:h, :w] = image
    return padded_img


def key_gen(key, size):
    digest = hashlib.sha256(key.encode('utf-8')).hexdigest()
    s1, s2, s3, s4 = [int(digest[8 * i:8 * i + 8], 16) for i in range(4)]
    np.random.seed(s1)
    k1 = np.random.permutation(size)
    np.random.seed(s2)
    k2 = np.random.randint(4, size=size)
    np.random.seed(s3)
    k3 = np.random.randint(4, size=size)
    np.random.seed(s4)
    k4 = np.random.randint(2, size=size)
    return [k1, k2, k3, k4]


def to_blocks(arr, rows, columns):
    h, w = arr.shape
    return arr.reshape(h // rows, rows, -1, columns).swapaxes(1, 2).reshape(-1, rows, columns)


def from_blocks(arr, h, w):
    n, rows, columns = arr.shape
    return arr.reshape(h // rows, -1, rows, columns).swapaxes(1, 2).reshape(h, w)
