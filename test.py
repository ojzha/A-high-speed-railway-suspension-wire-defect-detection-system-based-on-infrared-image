import multiprocessing
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import torch
import torchvision
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

from ultralytics import YOLO


class My_Thread( QThread ):
    _signal = pyqtSignal(str)
    def __init__(self , path):
        super().__init__()
        print("在初始化多线程")
        self.image_path = path

    def run(self):
        print("是MyThread线程中执行.")
        self._signal.emit("在处理啦>>>")

        model = YOLO('best.pt')
        self.results = model(self.image_path)

        file_path = './output.txt'
        with open(file_path, "w") as F:
            F.write( str(self.results) )

        self._signal.emit( str( self.results[0] ) )
        annotated_frame = self.results[0].plot()
        print("debug3")

        height, width, channel = annotated_frame.shape
        bytes_per_line = 3 * width
        self.qimage = QtGui.QImage(annotated_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.pixmap = QtGui.QPixmap.fromImage(self.qimage)

        print("其实已经跑完了")
        self._signal.emit("全部完成")

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self, MainWindow): # 设置界面的组件，包括主窗口、按钮、标签等
        MainWindow.setObjectName("MainWindow") #设置主窗口对象的名称为"MainWindow"。
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

    def retranslateUi(self, MainWindow):# 设置界面各个组件的文本内容。
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "上传图片"))
        self.pushButton_2.setText(_translate("MainWindow", "显示环境"))
        self.pushButton_3.setText(_translate("MainWindow", "启动程序"))
        self.label2.setText(_translate("MainWindow", "TextLabel"))
        self.label3.setText(_translate("MainWindow", "TextLabel"))
    #
    def uploadImage(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, '选择图片', '', 'Images (*.png *.xpm *.jpg *.bmp)')
        self.image_path = image_path
        print(self.image_path)
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
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setText("正在处理...")
        self.my_thread = My_Thread(self.image_path)
        self.my_thread._signal.connect(self.set_btn_resig)
        self.my_thread.start()

    def set_btn_resig(self , _info):
        if _info == "全部完成":
            self.label3.setPixmap(self.my_thread.pixmap)
            self.label3.setScaledContents(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_3.setText("开始处理")
        else:
            self.label1.setText(_info)


if __name__ == '__main__':
    # sys.stdout = open("output.txt", "w")
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)
    icon = QIcon('snake.png')  # 替换为你的图标文件路径
    app.setWindowIcon(icon)
    MainWindow1 = QMainWindow()     #MainWindow1随便改
    ui = Ui_MainWindow()             #随便改
    ui.setupUi(MainWindow1)
    MainWindow1.show()

    sys.exit(app.exec_())