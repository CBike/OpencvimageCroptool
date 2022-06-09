import threading

from PIL import Image
import time
import cv2
import numpy as np
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from function import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
area = []

class CWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Gvm_Image_Croptool")
        formbox = QVBoxLayout()
        self.setLayout(formbox)

        viewLayout = QVBoxLayout()
        controlLayout = QVBoxLayout()
        dataInputLayout = QVBoxLayout()


        self.pencolor = QColor(180, 85, 162)
        self.brushcolor = QColor(180, 85, 162, 0)

        self.btnread = QPushButton("Read")
        controlLayout.addWidget(self.btnread)
        self.btnCapture = QPushButton("Capture")
        controlLayout.addWidget(self.btnCapture)
        self.btnSave = QPushButton("Save")
        controlLayout.addWidget(self.btnSave)

        controlLayout.setStretchFactor(self.btnread, 1)
        controlLayout.setStretchFactor(self.btnCapture, 1)
        controlLayout.setStretchFactor(self.btnSave, 1)

        self.view = CView(self)
        viewLayout.addWidget(self.view)

        self.rdialog = Rdialog()

        self.lb_dataInput = QLabel("Data In Put Layout")
        dataInputLayout.addWidget(self.lb_dataInput)

        self.input_display_id = QLineEdit("INSERT DiSPLAY ID")
        dataInputLayout.addWidget(self.input_display_id)

        formbox.addLayout(viewLayout)
        formbox.addLayout(dataInputLayout)
        formbox.addLayout(controlLayout)


        formbox.setStretchFactor(viewLayout, 6)

        self.resize(1280, 720)
        self.center()

        self.btnread.pressed.connect(self.btn_read)
        self.btnSave.pressed.connect(self.btn_save)
        self.btnCapture.pressed.connect(self.btn_cap)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn_read(self):
        # filepath = Request_gvm_image(self.input_display_id.text())
        # self.view.refresh_view(filepath)
        self.view.refresh_view('')

    def btn_save(self):
        pass

    def btn_cap(self):
        self.rdialog.exec_()


class CView(QGraphicsView, QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.begin, self.destination = QPoint(), QPoint()

        self.pixmap = QPixmap()
        self.painter = QPainter(self)
        self.painter.drawPixmap(QPoint(), self.pixmap)



    def refresh_view(self, img):
        # self.pixmap.load(img)
        self.pixmap.load("C:\python_dev\imageCroptool(GVM)\\cat.png")
        self.scene.addPixmap(self.pixmap)
        self.setScene(self.scene)

    # def paintEvent(self, e):
    #     if not self.pixmap.isNull() and not self.begin.isNull() and not self.destination.isNull():
    #         rect = QRect(self.begin, self.destination)
    #         self.painter.drawRect(rect.normalized())

    def mousePressEvent(self, e):
        if not self.pixmap.isNull() and e.buttons() & Qt.LeftButton:
            self.begin = e.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, e):
        if not self.pixmap.isNull() and e.buttons() & Qt.LeftButton:
            self.destination = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if not self.pixmap.isNull() and e.buttons() & Qt.LeftButton:
            print('START POINT::', self.begin)
            print('END POINT::', self.destination)

class Rdialog(QDialog):
    def __int__(self):
        super(self).__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Captured Image")

        lb_refdata = QLabel("")
        self.btn_save = QPushButton("btn_save")
        self.btn_cancel = QPushButton("btn_cancel")

        layout = QGridLayout()
        layout.addWidget(lb_refdata, 0, 0)
        layout.addWidget(self.btn_save, 0, 2)
        layout.addWidget(self.btn_cancel, 0, 2)
        self.setLayout(layout)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    w.show()
    sys.exit(app.exec_())