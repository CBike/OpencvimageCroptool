import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextBrowser, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QRubberBand
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QPalette
import cv2
from function_TEST import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
img_origin = 'ADB.png'
GVM_DISPLAY = 'NOT DISPLAY IMAGE'



class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        self.window_width, self.window_height = 1200, 747
        self.setMinimumSize(self.window_width, self.window_height)

        self.lyt_main = QVBoxLayout()
        self.lyt_log = QVBoxLayout()
        self.lyt_view = QVBoxLayout()

        self.lyt_main.setContentsMargins(0, 0, 0, 0)
        self.lyt_main.setSpacing(1)

        self.pix = QPixmap()
        self.log = TextLog()
        self.lb_pixmap = QLabel()
        self.scrollArea = QScrollArea()

        self.init_ui()

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def init_ui(self):

        self.setWindowTitle("ADB_IMAGE_CROP_TOOL")
        self.setWindowIcon(QIcon("66804.png"))

        self.pixmap_load()

        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.lb_pixmap)
        self.scrollArea.setFixedSize(1920, 900)

        self.lyt_view.addWidget(self.scrollArea)
        self.lyt_log.addWidget(self.log)
        self.lyt_main.addLayout(self.lyt_view)
        self.lyt_main.addLayout(self.lyt_log)

        self.statusBar().showMessage("TOOL IS READY ! !")

        widget = QWidget()
        widget.setLayout(self.lyt_main)
        self.setCentralWidget(widget)

    def pixmap_change(self, image):

        global img_origin
        img_origin = image

    def pixmap_load(self):

        self.pix.load(img_origin)
        self.lb_pixmap.setPixmap(self.pix)
        self.lb_pixmap.setFixedSize(self.pix.size())
        self.update()


    def keyPressEvent(self, e):

        global GVM_DISPLAY
        if e.key() == Qt.Key_0:
            GVM_DISPLAY = 0
            filepath = Request_gvm_image(0)
            self.pixmap_change(filepath)
            self.pixmap_load()

        if e.key() == Qt.Key_1:
            GVM_DISPLAY = 1
            filepath = Request_gvm_image(1)
            self.pixmap_change(filepath)
            self.pixmap_load()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.statusBar().showMessage("GVM_DISPLAY :{}, POINTER {}.{}".
                                         format(GVM_DISPLAY, event.pos().x(), event.pos().y()))
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):

        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.statusBar().showMessage("GVM_DISPLAY :{} AND CORDINATE {}.{}:{}.{}"
                                         .format(GVM_DISPLAY, self.origin.x(), self.origin.y(), event.pos().x(), event.pos().y()))


    def mouseReleaseEvent(self, event):

        now = datetime.now()
        timestamp = now.strftime("%d_%H_%M_%S")

        if event.button() == Qt.LeftButton and not self.origin.x() == event.pos().x():
            print(self.origin.x(), self.origin.y(), event.pos().x(), event.pos().y())
            try:
                target = cv2.imread(img_origin)
                cropped_img = target[int(self.origin.y()):int(event.pos().y()), int(self.origin.x()):int(event.pos().x())]
                imgdir = r'.\captured_image\cropped_img_{}.bmp'.format(timestamp)
                cv2.imwrite(imgdir, cropped_img)
                self.log.le_log.append("ATS_COMMON_1.GVM_IMAGE({},{}[{}:{},{}:{}])".format(GVM_DISPLAY, os.path.abspath(imgdir)
                                                                                  ,int(self.origin.y()),int(event.pos().y()), int(self.origin.x()),int(event.pos().x())))
            except Exception as e:
                print(e)


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
    window = MainWindow()
    window.resize(1200, 747)
    window.show()
    app.exec_()