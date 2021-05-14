# -*- coding: utf-8 -*-
"""
# @FileName             : record_video.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""

import cv2 as cv
import settings


def record_video(out_file, device):
    cv.namedWindow("Video")
    cap = cv.VideoCapture(device)
    
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv.CAP_PROP_FPS))
    print(height, width, fourcc, fps)
    video_writer = cv.VideoWriter(out_file, fourcc, fps, (width, height))
    if not cap.isOpened():
        raise Exception("can not opened")
    ret, srcImage = cap.read()
    while ret:
        cv.imshow("Video", srcImage)
        video_writer.write(srcImage)
        if cv.waitKey(1000 // fps) & 0xFF == 27:
            break
        ret, srcImage = cap.read()


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))
    record_video("test_record_video2.mp4", 0)
