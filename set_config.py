import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtCore as QtCore
import config

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.okButton = QPushButton("Save")
        self.okButton.setStyleSheet('background: rgb(255, 170, 255);')
        self.okButton.clicked.connect(self.save)

        self.text = QLabel('Text color')
        self.key = QLabel('Key color')
        self.thickness = QLabel('Border thickness')
        self.distance = QLabel('Pressing distance')


        self.textEdit = QLineEdit()
        self.textEdit.setText(str(config.COLOR_OUT_UP))
        self.keyEdit = QLineEdit()
        self.keyEdit.setText(str(config.COLOR_IN_DOWN))
        self.thicknessEdit = QLineEdit()
        self.thicknessEdit.setText(str(config.KEY_BORDER))
        self.distanceEdit = QLineEdit()
        self.distanceEdit.setText(str(config.THRESHOLD_PRESS))

        self.textEdit.setStyleSheet('background: rgb(255, 119, 224);')
        self.keyEdit.setStyleSheet('background: rgb(255, 119, 224);')
        self.thicknessEdit.setStyleSheet('background: rgb(255, 119, 224);')
        self.distanceEdit.setStyleSheet('background: rgb(255, 119, 224);')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.text, 1, 0)
        grid.addWidget(self.textEdit, 1, 1)

        grid.addWidget(self.key, 2, 0)
        grid.addWidget(self.keyEdit, 2, 1)

        grid.addWidget(self.thickness, 3, 0)
        grid.addWidget(self.thicknessEdit, 3, 1)

        grid.addWidget(self.distance, 4, 0)
        grid.addWidget(self.distanceEdit, 4, 1)

        grid.addWidget(self.okButton, 5, 1)

        self.setLayout(grid)

        self.setStyleSheet('background: rgb(255, 201, 253);')
        self.resize(220, 300)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon('img/icon.png'))
        self.show()

    def save(self):
        a = self.keyEdit.text()
        b = self.textEdit.text()
        v = self.distanceEdit.text()
        g = self.thicknessEdit.text()
        print(a, b, v, g)
        text = f"""FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16
PINKY_TIP = 20

THRESHOLD_PRESS = {v}

TRACK_FINGERS = [INDEX_FINGER_TIP]

WAIT_TIME = 8

COLOR_IN_DOWN = COLOR_IN_UP = {a}
COLOR_OUT_DOWN = COLOR_OUT_UP = {b}
KEY_BORDER = {g}

CURSOR_DOWN = (0, 0, 0)
CURSOR_UP = COLOR_OUT_DOWN
# CURSOR_UP = (255 - COLOR_OUT_DOWN[0], 255 - COLOR_OUT_DOWN[1], 255 - COLOR_OUT_DOWN[2])"""
        config_file = open("config.py", "w")
        config_file.write(text)
        config_file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
