import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import torch
import torchvision
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow, QLabel, QTextBrowser

from ultralytics import YOLO


class MyThread(QThread):
    update_signal = pyqtSignal(str, QPixmap)

    def __init__(self, image_path=''):
        super().__init__()
        self.image_path = image_path

    def run(self):
        self.update_signal.emit("正在处理图片...", None)

        model = YOLO('best.pt')
        results = model(self.image_path)
        annotated_frame = results[0].plot()

        height, width, channel = annotated_frame.shape
        bytes_per_line = 3 * width
        qimage = QImage(annotated_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        self.update_signal.emit(self.image_path, pixmap)


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.my_Thread = None

    def setupUi(self, MainWindow):
        # ... (略去未修改部分)
        MainWindow.setObjectName("MainWindow")  # 设置主窗口对象的名称为"MainWindow"。
        MainWindow.resize(1128, 1009)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 10, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 10, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(20, 60, 1071, 71))
        self.label1.setObjectName("label1")
        # self.label1 = QtWidgets.QTextBrowser(self.centralwidget)
        # self.label1.setGeometry(QtCore.QRect(20, 60, 1071, 71))
        # self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(40, 190, 481, 421))
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(600, 200, 461, 381))
        self.label3.setObjectName("label3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 点击响应函数
        self.pushButton.clicked.connect(self.uploadImage)
        self.pushButton_2.clicked.connect(self.showEnvironment)
        self.pushButton_3.clicked.connect(self.startProgram)
        self.image_path = ''

    def retranslateUi(self, MainWindow):# 设置界面各个组件的文本内容。
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "上传图片"))
        self.pushButton_2.setText(_translate("MainWindow", "显示环境"))
        self.pushButton_3.setText(_translate("MainWindow", "启动程序"))
        self.label2.setText(_translate("MainWindow", "TextLabel"))
        self.label3.setText(_translate("MainWindow", "TextLabel"))

    def uploadImage(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, '选择图片', '', 'Images (*.png *.xpm *.jpg *.bmp)')
        self.image_path = image_path
        if image_path:
            # 在这里添加加载图片的逻辑，例如显示图片到label2
            pixmap = QtGui.QPixmap(image_path)
            self.label2.setPixmap(pixmap)
            self.label2.setScaledContents(True)
        self.label1.setText("不知道发生了什么 看看有没有运行这个方法")

    def showEnvironment(self):
        pytorch_version = torch.__version__
        torchvision_version = torchvision.__version__
        self.label1.setText(f"PyTorch Version: {pytorch_version}\n"
                            f"Torchvision Version: {torchvision_version}")

    def startProgram(self):
        if not self.my_Thread or not self.my_Thread.isRunning():
            self.my_Thread = MyThread(self.image_path)
            self.my_Thread.update_signal.connect(self.updateUI)
            self.my_Thread.start()
        else:
            self.label1.setText("程序已经在运行中，请等待完成。")


    def updateUI(self, message, pixmap):
        self.label1.setText(message)
        if pixmap:
            self.label3.setPixmap(pixmap)
            self.label3.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon = QIcon('snake.png')
    app.setWindowIcon(icon)
    MainWindow1 = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow1)
    MainWindow1.show()
    sys.exit(app.exec_())
