# -*- coding: utf-8 -*-
"""
# @FileName             : utils.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""
import math
import cv2 as cv
import numpy as np


def hisEqulColor(img):
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    channels = cv.split(ycrcb)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])
    cv.merge(channels, ycrcb)
    cv.cvtColor(ycrcb, cv.COLOR_YCR_CB2BGR, img)
    return img


def resizeRatio(image, newHeight: int = None, newWidth: int = None, interpolation=None):
    height, width = image.shape[0], image.shape[1]

    if newHeight and newWidth:
        # 宽高同时不为空
        raise Exception("不能同时指定宽和高")

    if not newHeight and not newHeight:
        # 宽高同时为空
        newHeight = height

    if not newHeight:
        newHeight = int(height * (newWidth / width))
    if not newWidth:
        newWidth = int(width * (newHeight / height))

    return cv.resize(image, (newWidth, newHeight), interpolation=interpolation)


def createCircleKernel(size: int):
    kernel = np.ones((size, size), np.uint8)
    re_kernel = []
    rows, cols = kernel.shape
    for i in range(rows):
        result = [0 if math.sqrt((i - size // 2) ** 2 + (j - size // 2) ** 2) > size // 2 else 1 for j in range(cols)]
        re_kernel.append(result)
    re_kernel = np.array(re_kernel, np.uint8)
    return re_kernel


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))


    def test_createCircleKernel():
        kernel = createCircleKernel(3)
        test_kernel = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        rows, cols = kernel.shape
        for i in range(rows):
            for j in range(cols):
                assert kernel[i][j] == test_kernel[i][j]


    test_createCircleKernel()
