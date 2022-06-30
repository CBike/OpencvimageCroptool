from PyQt5.QtCore import QPoint, QRect, QSize, Qt
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QWidget, QLabel, QRubberBand
from PyQt5.QtGui import *


class Window(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.setFixedSize(411, 247)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):

        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
            print(self.origin.x(), self.origin.y(), event.pos().x(), event.pos().y())
            print(self.origin - QPoint(20, 20))
            print(self.origin.x(), self.origin.y(), event.pos().x(), event.pos().y())


app = QApplication(sys.argv)
myWindow = Window(None)
myWindow.show()
app.exec_()
