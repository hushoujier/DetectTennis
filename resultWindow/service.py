# -*- coding: utf-8 -*-
"""
# @FileName             : service.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""

from PySide2.QtWidgets import QLabel
from pyside2mvcframework.core.service import Service
from utils import hisEqulColor
from .model import ResultModel
import settings
import cv2 as cv


class ResultService(Service):

    def __init__(self, device: str):
        self.cap = cv.VideoCapture(device)
        self.model = ResultModel()

    def drawLabel(self, label: QLabel):

        pass

    def detectTennis(self):
        if not self.cap.isOpened():
            raise Exception("can not opened")
        ret, srcImage = self.cap.read()
        while ret:
            hisFrame = hisEqulColor(srcImage) if settings.HIS_EQU_COLOR else srcImage
            gFrame = cv.GaussianBlur(hisFrame,
                                     settings.GAUSSIAN_BLUR_KSIZE,
                                     sigmaX=settings.GAUSSIAN_BLUR_SIGMAX,
                                     sigmaY=settings.GAUSSIAN_BLUR_SIGMAY) \
                if settings.GAUSSIAN_BLUR_KSIZE is not None else hisFrame
            bFrame = cv.blur(gFrame, settings.BLUR_KSIZE) if settings.BLUR_KSIZE else gFrame
            mFrame = cv.medianBlur(bFrame,
                                   settings.MEDIAN_BLUR_KSIZE) \
                if settings.MEDIAN_BLUR_KSIZE else bFrame
            hsvFrame = cv.cvtColor(mFrame, cv.COLOR_BGR2HSV)
            inRangeFrame = cv.inRange(hsvFrame, settings.HSV_LOWER, settings.HSV_UPPER)
            dilateFrame = cv.dilate(inRangeFrame,
                                    settings.DILATE_KERNEL,
                                    iterations=settings.DILATE_ITERATIONS) \
                if settings.DILATE_KERNEL else inRangeFrame
            erodeFrame = cv.erode(dilateFrame,
                                  settings.ERODE_KERNEL,
                                  iterations=settings.ERODE_ITERATIONS) \
                if settings.ERODE_KERNEL else dilateFrame

            contours, h = cv.findContours(erodeFrame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contoursCircles = []
            for c in contours:
                (x, y), radius = cv.minEnclosingCircle(c)
                area = settings.PI * radius * radius
                if cv.contourArea(c) > area * settings.AREA_RATE:
                    contoursCircles.append([x, y, radius, 0])
            print("contoursCircles:{}".format(len(contoursCircles)))
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
            print(contoursCircles)
            print(trueCircles)
            for x, y, r, v in trueCircles:
                cv.circle(srcImage, (int(x), int(y)), int(r), (0, 0, 255), 2)
                cv.circle(srcImage, (int(x), int(y)), 1, (0, 0, 255), 1)
            self.model.cvMatResult = srcImage
            ret, srcImage = self.cap.read()


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))
