from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore


class WindowView(QMainWindow):
    def __init__(self, parent, name):
        super(WindowView, self).__init__(parent)
        self.setupUi(self)
        self.web = QWebEngineView()
        self.web.setHtml(open(name, encoding="utf-8").read())
        self.setCentralWidget(self.web)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle('Просмотр графа')
        MainWindow.setGeometry(300, 250, 1615, 900)
        MainWindow.setStyleSheet("background-color: rgb(66, 72, 116);\n"
                                 "color: rgb(244, 238, 255);\n"
                                 "")
        MainWindow.centralwidget = QtWidgets.QWidget(self)
        MainWindow.centralwidget.setObjectName("centralwidget")
        MainWindow.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        MainWindow.gridLayout.setObjectName("gridLayout")
        MainWindow.frame = QtWidgets.QFrame(self.centralwidget)
        MainWindow.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        MainWindow.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        MainWindow.frame.setObjectName("frame")
        # MainWindow.pushButton = QtWidgets.QPushButton(self.frame)
        # MainWindow.pushButton.setGeometry(QtCore.QRect(700, 800, 200, 50))
        # MainWindow.pushButton.setStyleSheet("font: 12pt \"Cambria\";\n"
        #                               "color: rgb(0,0,0);\n"
        #                               "background-color: rgb(244, 238, 255);\n"
        #                               "border-radius: 10%")
        # MainWindow.pushButton.setObjectName("pushButton")
        # MainWindow.pushButton.setText("Построить граф")

    # def save_graph(self):
        # описать сохранение полученного графа
        # try:
            # res = QFileDialog.getOpenFileName(self, 'Open File', '/Users', filter='Text Files (*.txt)')
            # path1 = res[0]
            # txt_content = open(path1, 'r', encoding="utf-8").read()
            # self.hide()
            # self.redact = WindowRedact(self, txt_content)
           # self.redact.show()
        # except Exception:
        #     print("Файл не был выбран.")
