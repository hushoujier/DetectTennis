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
    def hMinChange(x):
        settings.HSV_LOWER[0] = x

    def sMinChange(x):
        settings.HSV_LOWER[1] = x

    def vMinChange(x):
        settings.HSV_LOWER[2] = x

    def hMaxChange(x):
        settings.HSV_UPPER[0] = x

    def sMaxChange(x):
        settings.HSV_UPPER[1] = x

    def vMaxChange(x):
        settings.HSV_UPPER[2] = x

    num = 1
    stop = False
    cap = cv.VideoCapture(settings.DEVICE)
    print(cap.get(cv.CAP_PROP_FRAME_WIDTH), cap.get(cv.CAP_PROP_FRAME_HEIGHT), cap.get(cv.CAP_PROP_FPS))
    if not cap.isOpened():
        raise Exception("can not opened")
    ret, srcImage = cap.read()
    in_time = time.time()
    cv.namedWindow("resultWindow")
    cv.namedWindow("inRange")

    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv.CAP_PROP_FPS))
    save_file = "mark2.mp4"

    video_writer = cv.VideoWriter(save_file, fourcc, fps, (width, height))
    cv.createTrackbar("hMin", "inRange", 0, 180, hMinChange)
    cv.setTrackbarPos("hMin", "inRange", settings.HSV_LOWER[0])
    cv.createTrackbar("sMin", "inRange", 0, 255, sMinChange)
    cv.setTrackbarPos("sMin", "inRange", settings.HSV_LOWER[1])
    cv.createTrackbar("vMin", "inRange", 0, 255, vMinChange)
    cv.setTrackbarPos("vMin", "inRange", settings.HSV_LOWER[2])
    cv.createTrackbar("hMax", "inRange", 0, 180, hMaxChange)
    cv.setTrackbarPos("hMax", "inRange", settings.HSV_UPPER[0])
    cv.createTrackbar("sMax", "inRange", 0, 255, sMaxChange)
    cv.setTrackbarPos("sMax", "inRange", settings.HSV_UPPER[1])
    cv.createTrackbar("vMax", "inRange", 0, 255, vMaxChange)
    cv.setTrackbarPos("vMax", "inRange", settings.HSV_UPPER[2])
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
        cv.imshow("inRange", inRangeFrame)
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
                contoursCircles.append([x, y, radius, 1])
        print("contoursCircles:{}个,分别为{}".format(len(contoursCircles), contoursCircles))
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
        print("houghCircles:{}个".format(len(houghCircles)))
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
        print("trueCircles", trueCircles)
        for x, y, r, v in trueCircles:
            cv.circle(srcFrame, (int(x), int(y)), int(r), (0, 0, 255), 2)
            cv.circle(srcFrame, (int(x), int(y)), 1, (0, 0, 255), 1)
            cv.putText(srcFrame,
                       "(x={},y={},r={})".format(int(x), int(y), int(r)), (int(x - r), int(y - r)),
                       cv.FONT_HERSHEY_COMPLEX_SMALL,
                       0.6,
                       (255, 0, 0))
        cv.imshow("resultWindow", srcFrame)

        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
        if k == 32:
            stop = True if stop is False else False

        if stop is False:
            video_writer.write(srcFrame)
            ret, srcImage = cap.read()
            num = num + 1
        else:
            time.sleep(0.1)
    out_time = time.time()
    print(num // int(out_time - in_time))


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))
    detectTennis()
