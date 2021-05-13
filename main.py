# -*- coding: utf-8 -*-
"""
# @FileName             : main.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""
import time
from utils import hisEqulColor
import settings
import cv2 as cv


def detectTennis():
    num = 0
    cap = cv.VideoCapture(settings.DEVICE)
    print(cap.get(cv.CAP_PROP_FRAME_WIDTH),cap.get(cv.CAP_PROP_FRAME_HEIGHT),cap.get(cv.CAP_PROP_FPS))
    if not cap.isOpened():
        raise Exception("can not opened")
    ret, srcImage = cap.read()
    in_time = time.time()
    cv.namedWindow("resultWindow")
    while ret:
        srcFrame = srcImage.copy()
        hisFrame = hisEqulColor(srcFrame) if settings.HIS_EQU_COLOR else srcFrame
        gFrame = cv.GaussianBlur(hisFrame,
                                 settings.GAUSSIAN_BLUR_KSIZE,
                                 sigmaX=settings.GAUSSIAN_BLUR_SIGMAX,
                                 sigmaY=settings.GAUSSIAN_BLUR_SIGMAY) \
            if settings.GAUSSIAN_BLUR_KSIZE is not None else hisFrame
        bFrame = cv.blur(gFrame,
                         settings.BLUR_KSIZE) \
            if settings.BLUR_KSIZE is not None else gFrame
        mFrame = cv.medianBlur(bFrame,
                               settings.MEDIAN_BLUR_KSIZE) \
            if settings.MEDIAN_BLUR_KSIZE is not None else bFrame
        hsvFrame = cv.cvtColor(mFrame, cv.COLOR_BGR2HSV)
        inRangeFrame = cv.inRange(hsvFrame, settings.HSV_LOWER, settings.HSV_UPPER)
        dilateFrame = cv.dilate(inRangeFrame,
                                settings.DILATE_KERNEL,
                                iterations=settings.DILATE_ITERATIONS) \
            if settings.DILATE_KERNEL is not None else inRangeFrame
        erodeFrame = cv.erode(dilateFrame,
                              settings.ERODE_KERNEL,
                              iterations=settings.ERODE_ITERATIONS) \
            if settings.ERODE_KERNEL is not None else dilateFrame

        contours, h = cv.findContours(erodeFrame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contoursCircles = []
        for c in contours:
            (x, y), radius = cv.minEnclosingCircle(c)
            area = settings.PI * radius * radius
            if cv.contourArea(c) > area * settings.AREA_RATE:
                contoursCircles.append([x, y, radius, 0])
        houghCircles = cv.HoughCircles(erodeFrame,
                                       method=settings.METHOD,
                                       dp=settings.DP,
                                       minDist=settings.MIN_DIST,
                                       param1=settings.PARAM1,
                                       param2=settings.PARAM2,
                                       minRadius=settings.MIN_RADIUS,
                                       maxRadius=settings.MAX_RADIUS)
        if houghCircles is not None:
            houghCircles = houghCircles[0, :]
        else:
            houghCircles = []

        for hc in houghCircles:
            for cc in contoursCircles:
                if abs(cc[0] - hc[0]) < settings.MAX_ABS_X \
                        and abs(cc[1] - hc[1]) < settings.MAX_ABS_Y \
                        and abs(cc[2] - hc[2]) < settings.MAX_ABS_R:
                    cc[3] += 1
        trueCircles = []
        for cc in contoursCircles:
            if cc[3] > settings.MIN_VOTE:
                trueCircles.append(cc)
        for x, y, r, v in trueCircles:
            cv.circle(srcImage, (int(x), int(y)), int(r), (0, 0, 255), 2)
            cv.circle(srcImage, (int(x), int(y)), 1, (0, 0, 255), 1)
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
    detectTennis()
