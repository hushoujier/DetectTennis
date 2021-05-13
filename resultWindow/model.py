# -*- coding: utf-8 -*-
"""
# @FileName             : model.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""
from pyside2mvcframework.core.model import Model
from pyside2mvcframework.core.model import Data


class ResultModel(Model):
    cvMatResult = Data()


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))
