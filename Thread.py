import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class WorkerThread(QThread):
    finished = pyqtSignal()

    def run(self):
        # 在这里执行需要在新线程中完成的工作
        # 例如，调用 startProgram 方法
        main_window.startProgram()
        self.finished.emit()


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('多线程示例')

        self.label = QLabel('等待启动...')
        self.btnStart = QPushButton('启动程序')
        self.btnStart.clicked.connect(self.startThread)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btnStart)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def startThread(self):
        # 创建并启动工作线程
        self.workerThread = WorkerThread()
        self.workerThread.finished.connect(self.threadFinished)
        self.workerThread.start()

        # 更新界面
        self.label.setText('程序启动中...')
        self.btnStart.setEnabled(False)

    def threadFinished(self):
        # 工作线程完成后的操作
        self.label.setText('程序已启动！')
        self.btnStart.setEnabled(True)


    def startProgram(self):
        # 模拟长时间运行的任务
        time.sleep(5)
        print("程序已启动！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.setGeometry(100, 100, 400, 200)
    main_window.show()
    sys.exit(app.exec_())
