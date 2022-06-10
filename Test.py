import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from function_TEST import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
img_origin = ''

class MyApp(QWidget):
    def __init__(self):
        super(MyApp, self).__init__()
        self.window_width, self.window_height = 1280, 720
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pix = QPixmap()
        self.pix.load(img_origin)

        self.begin, self.destination = QPoint(), QPoint()




    def pixmap_reload(self):
        self.pix = QPixmap()
        self.pix.load(img_origin)
        self.update()

    def pixmap_change(self, image):
        global img_origin
        img_origin = image
        self.pixmap_reload()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.green)
        painter.drawPixmap(QPoint(), self.pix)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())

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
            target = self.image_crop()
            self.save_img(target)

    def keyPressEvent(self, e):
        global img_origin
        if e.key() == Qt.Key_0:
            filepath = Request_gvm_image(0)
            print(filepath)
            self.pixmap_change(filepath)
        if e.key() == Qt.Key_1:
            filepath = Request_gvm_image(1)
            print(filepath)
            self.pixmap_change(filepath)

    def image_crop(self):

        target = cv2.imread(img_origin)
        cropped_img = target[self.begin.y():self.destination.y(), self.begin.x():self.destination.x()]
        self.showmessageBox()

        return cropped_img

    def save_img(self, cropped_img):

        now = datetime.now()
        timestamp = now.strftime("%d_%H_%M_%S")
        cv2.imwrite('.\captured_image\cropped_img_{}.bmp'.format(timestamp), cropped_img)

    def showmessageBox(self):

        msgBox = QMessageBox()
        msgBox.setWindowTitle("INFORMATION")
        msgBox.setText("View Captured Cordinate in details")
        msgBox.setDetailedText('Captured Image Cordinate [{}:{},{}:{}]'.
                             format(self.begin.y(), self.destination.y(), self.begin.x(), self.destination.x()))
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        Qwidget {
            font-size: 30px;
        }''')
    myApp = MyApp()
    myApp.show()

    app.exec_()
