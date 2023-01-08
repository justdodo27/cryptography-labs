import numpy as np
import random as rn

def set_pixels(part, i, j, key_row):
    part[i * 2][j * 2] = key_row[0].astype(bool)
    part[i * 2][j * 2 + 1] = key_row[1].astype(bool)
    part[i * 2 + 1][j * 2] = key_row[2].astype(bool)
    part[i * 2 + 1][j * 2 + 1] = key_row[3].astype(bool)

def create_parts(image):
    part_1 = np.ones((image.shape[0]*2, image.shape[1]*2))
    part_2 = np.ones((image.shape[0]*2, image.shape[1]*2))

    c0 = np.array([
        [
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ],
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0]
        ],
        [
            [0, 1, 0, 1],
            [0, 1, 0, 1]
        ],
        [
            [1, 0, 1, 0],
            [1, 0, 1, 0]
        ],
        [
            [0, 1, 1, 0],
            [0, 1, 1, 0]
        ],
        [
            [1, 0, 0, 1],
            [1, 0, 0, 1]
        ],
    ])

    c1 = np.array([
        [
            [0, 0, 1, 1],
            [1, 1, 0, 0]
        ],
        [
            [1, 1, 0, 0],
            [0, 0, 1, 1]
            
        ],
        [
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ],
        [
            [1, 0, 1, 0],
            [0, 1, 0, 1]
        ],
        [
            [0, 1, 1, 0],
            [1, 0, 0, 1]
        ],
        [
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ],
    ])

    for i in range(image.shape[0]):
        for j in range(image.shape[1] - 1):
            r = rn.randint(0, 5)
            if image[i][j] < 128: #black pixel
                set_pixels(part_1, i, j, c1[r, 0])
                set_pixels(part_2, i, j, c1[r, 1])
            else: #white pixel
                set_pixels(part_1, i, j, c0[r, 0])
                set_pixels(part_2, i, j, c0[r, 1])

    return part_1, part_2