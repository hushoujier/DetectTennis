# -*- coding: utf-8 -*-
"""
# @FileName             : main.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""
import time
import cv2 as cv


def test_video_fps():
    num = 0
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("can not opened")
    ret, srcImage = cap.read()
    in_time = time.time()
    while ret:
        #cv.imshow("resultWindow", srcImage)

        #k = cv.waitKey(1) & 0xFF
        #if k == 27:
        #    break
        ret, srcImage = cap.read()
        num=num+1
        now = time.time()
        if now-in_time > 100:
            break
        print(num)
    out_time=time.time()
    print(num//int(out_time-in_time))
    


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))
    test_video_fps()
