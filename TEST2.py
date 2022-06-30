import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from function_TEST import *
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
img_origin = 'ADB.png'


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)
        self.pix = QPixmap()
        self.lb_pixmap = QLabel()
        self.le_log = QTextBrowser()
        self.painter = QPainter(self)
        self.begin, self.destination = QPoint(), QPoint()



        widget = QWidget()
        lyt_main = QVBoxLayout(widget)
        lyt_log = QVBoxLayout()
        lyt_view = QVBoxLayout()
        lyt_view.addWidget(self.lb_pixmap)
        lyt_log.addWidget(self.le_log)
        lyt_main.addLayout(lyt_view)
        lyt_main.addLayout(lyt_log)

        self.setCentralWidget(widget)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ADB_IMAGE_CROP_TOOL")
        self.setWindowIcon(QIcon("66804.png"))
        self.statusBar().showMessage("Ready")
        self.pix.load(img_origin)
        self.lb_pixmap.setPixmap(self.pix)

    def pixmap_reload(self):
        self.pix = QPixmap()
        self.pix.load(img_origin)
        self.lb_pixmap.setPixmap(self.pix)
        self.update()

    def pixmap_change(self, image):
        global img_origin
        img_origin = image
        self.pixmap_reload()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_0:
            filepath = Request_gvm_image(0)
            print(filepath)
            self.pixmap_change(filepath)
            self.statusBar().showMessage("GVM_DISPLAY:0")

        if e.key() == Qt.Key_1:
            filepath = Request_gvm_image(1)
            print(filepath)
            self.pixmap_change(filepath)
            self.statusBar().showMessage("GVM_DISPLAY:1")

    def paintEvent(self, e):
        try:
            self.painter.setPen(Qt.green)
            self.painter.drawPixmap(QPoint(), self.pix)
            if not self.begin.isNull() and not self.destination.isNull():
                rect = QRect(self.begin, self.destination)
                self.painter.drawRect(rect.normalized())
        except Exception as e:
            print(e)
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
            # target = self.image_crop()
            # self.save_img(target)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()