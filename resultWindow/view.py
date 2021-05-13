# -*- coding: utf-8 -*-
"""
# @FileName             : view.py
# @Author               : 胡守杰
# @Email                : 2839414139@qq.com
# @ZhFileDescription    : 
# @EnFileDescription    : 
"""
import os
from pyside2mvcframework.core.view import View
from settings import PROJECT_PATH


class ResultWindowView(View):
    uiFilePath = os.path.join(PROJECT_PATH, "resultWindow/dResultWindow.ui")


if __name__ == '__main__':
    print("unit test from {filename}".format(filename=__file__))
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    view = ResultWindowView().birth()
    view.show()
    sys.exit(app.exec_())
