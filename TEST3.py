import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextBrowser, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QPalette
import cv2
from function_TEST import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
img_origin = 'ADB.png'
GVM_DISPLAY = ''
pointer = ''


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        widget = QWidget()
        self.lyt_main = QVBoxLayout()
        self.lyt_log = QVBoxLayout()
        self.lyt_view = QVBoxLayout()

        self.lyt_main.setContentsMargins(0, 0, 0, 0)
        self.lyt_main.setSpacing(0)

        self.lyt_view.addWidget(PixMap())
        self.lyt_log.addWidget(TextLog())

        self.lyt_main.addLayout(self.lyt_view)
        self.lyt_main.addLayout(self.lyt_log)

        widget.setLayout(self.lyt_main)
        self.setCentralWidget(widget)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ADB_IMAGE_CROP_TOOL")
        self.setWindowIcon(QIcon("66804.png"))
        self.statusBar().showMessage("Ready")

    def keyPressEvent(self, e):
        global img_origin

        try:
            if e.key() == Qt.Key_0:
                filepath = Request_gvm_image(0)
                img_origin = filepath
                self.lyt_view.addWidget()
                self.lyt_view.addWidget(PixMap())
                self.update()
                self.statusBar().showMessage("GVM_DISPLAY:0")

            if e.key() == Qt.Key_1:
                filepath = Request_gvm_image(1)
                img_origin = filepath
                self.lyt_view.addWidget(PixMap())
                self.update()
                self.statusBar().showMessage("GVM_DISPLAY:1")
        except Exception as e:
            print(e)






class PixMap(QWidget):
    def __init__(self):
        super(PixMap, self).__init__()
        self.lyt = QVBoxLayout()
        self.lyt.setContentsMargins(0, 0, 0, 0)
        self.lyt.setSpacing(0)

        self.lb_pixmap = QLabel()
        self.pix = QPixmap()
        self.pix.load(img_origin)
        self.lb_pixmap.setPixmap(self.pix)
        self.lyt.addWidget(self.lb_pixmap)

        self.begin, self.destination = QPoint(), QPoint()
        self.setLayout(self.lyt)

    def pixmap_reload(self):
        self.pix = QPixmap()
        self.pix.load(img_origin)
        self.lb_pixmap.setPixmap(self.pix)
        self.lb_pixmap.setFixedSize(self.pix.size())
        self.update()

    def pixmap_change(self, image):
        global img_origin
        img_origin = image
        self.pixmap_reload()

    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.begin = e.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.destination = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if not e.buttons() & Qt.LeftButton:
            print(self.begin)
            print(self.destination)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.green)
        painter.drawPixmap(QPoint(), self.pix)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())




class TextLog(QWidget):
    def __init__(self):
        super(TextLog, self).__init__()
        self.lyt = QVBoxLayout()

        self.le_log = QTextBrowser()
        self.le_log.setText("HELLO")

        self.lyt.addWidget(self.le_log)
        self.setLayout(self.lyt)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()