from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5 import QtWidgets, QtCore
import wikipediaapi  # pip install wikipedia-api
from window_redact import WindowRedact
from tqdm import tqdm
import concurrent.futures
import pandas as pd


class WindowStart(QMainWindow):
    def __init__(self):
        super(WindowStart, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.choose_file)
        self.pushButton_2.clicked.connect(self.wiki_scrape)
        self.redact = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 461)
        MainWindow.setStyleSheet("background-color: rgb(66, 72, 116);\n"
                                 "color: rgb(244, 238, 255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(66, 72, 116);\n"
                                 "color: rgb(244, 238, 255)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(260, 30, 200, 50))
        self.pushButton.setStyleSheet("font: 12pt \"Cambria\";\n"
                                      "color: rgb(0,0,0);\n"
                                      "background-color: rgb(244, 238, 255);\n"
                                      "border-radius: 10%")
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(220, 210, 441, 31))
        self.textEdit.setStyleSheet("background-color: rgb(244, 238, 255);\n"
                                    "font: 12pt \"Cambria\";\n"
                                    "color: rgb(0,0,0);")
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(70, 210, 141, 31))
        self.label.setStyleSheet("font: 12pt \"Cambria\";\n"
                                 "color: rgb(0,0,0);\n"
                                 "background-color: rgb(166, 177, 225)")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(340, 110, 41, 31))
        self.label_2.setStyleSheet("font: 75 14pt \"Cambria\";\n"
                                   "font-weight: bold;\n"
                                   "color: rgb(244, 238, 255)")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(70, 270, 151, 31))
        self.label_3.setStyleSheet("font: 12pt \"Cambria\";\n"
                                   "color: rgb(0,0,0);\n"
                                   "background-color: rgb(166, 177, 225)")
        self.label_3.setObjectName("label_3")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_2.setGeometry(QtCore.QRect(220, 270, 111, 31))
        self.textEdit_2.setStyleSheet("background-color: rgb(244, 238, 255);\n"
                                      "color: rgb(0,0,0);\n"
                                      "font: 12pt \"Cambria\";")
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(20, 170, 681, 231))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("background-color:rgb(166, 177, 225);\n"
                                   "border-radius: 10%")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 330, 151, 41))
        self.pushButton_2.setStyleSheet("font: 12pt \"Cambria\";\n"
                                        "color: rgb(0,0,0);\n"
                                        "background-color: rgb(244, 238, 255);\n"
                                        "border-radius: 10%")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4.raise_()
        self.pushButton.raise_()
        self.textEdit.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.textEdit_2.raise_()
        self.pushButton_2.raise_()
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выбор исходного текста"))
        self.pushButton.setText(_translate("MainWindow", "Выбрать локальный файл"))
        self.pushButton_2.setText(_translate("MainWindow", "Искать"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>Поисковой запрос: </p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "или"))
        self.label_3.setText(_translate("MainWindow", "Количество статей:"))

    def choose_file(self):
        try:
            res = QFileDialog.getOpenFileName(self, 'Open File', filter='Text Files (*.txt)')
            path1 = res[0]
            txt_content = open(path1, 'r', encoding="utf-8").read()
            self.hide()
            self.redact = WindowRedact(self, txt_content)
            self.redact.show()
        except:
            print("Файл не был выбран.")

    def wiki_page(self):
        wiki_api = wikipediaapi.Wikipedia(user_agent='KG auto-building (merlin@example.com)', language='ru',
                                          extract_format=wikipediaapi.ExtractFormat.WIKI)
        page_name = self.textEdit.toPlainText()
        page_name = wiki_api.page(page_name)
        if not page_name.exists():
            print('Page {} does not exist.'.format(page_name))
            return
        #
        # page_data = pd.DataFrame({
        #     'page': page_name,
        #     'text': page_name.text,
        #     'link': page_name.fullurl,
        #     'categories': [[y[9:] for y in
        #                     list(page_name.categories.keys())]],
        # })
        self.hide()
        self.redact = WindowRedact(self, page_name.text)
        self.redact.show()
        # return page_data

    def wiki_scrape(self, verbose=True):
        def wiki_link(link):
            try:
                page = wiki_api.page(link)
                if page.exists():
                    return {'page': link, 'text': page.text, 'link': page.fullurl,
                            'categories': list(page.categories.keys())}
            except:
                return None

        topic_name = self.textEdit.toPlainText()
        wiki_api = wikipediaapi.Wikipedia(user_agent='KG system (bk@example.com)', language='ru',
                                          extract_format=wikipediaapi.ExtractFormat.WIKI)
        page_name = wiki_api.page(topic_name)
        if not page_name.exists():
            print('Page {} does not exist.'.format(topic_name))
            return

        articles = int(self.textEdit_2.toPlainText())
        page_links = list(page_name.links.keys())
        progress = tqdm(desc='Links Scraped', unit='', total=len(page_links)) if verbose else None
        sources = [{'page': topic_name, 'text': page_name.text, 'link': page_name.fullurl,
                    'categories': list(page_name.categories.keys())}]

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_link = {executor.submit(wiki_link, link): link for link in page_links}
            for future in concurrent.futures.as_completed(future_link):
                data = future.result()
                sources.append(data) if data else None
                progress.update(1) if verbose else None
        progress.close() if verbose else None

        namespaces = ('Wikipedia', 'Special', 'Talk', 'LyricWiki', 'File', 'MediaWiki',
                      'Template', 'Help', 'User', 'Category talk', 'Portal talk')
        sources = pd.DataFrame(sources)
        sources = sources[(len(sources['text']) > 20)
                          & ~(sources['page'].str.startswith(namespaces, na=True))]
        sources['categories'] = sources.categories.apply(lambda x: [y[9:] for y in x])
        sources['topic'] = topic_name
        print('Wikipedia pages scraped:', len(sources))

        result_text = ''
        for i in range(articles):
            result_text += sources.iloc[i]['text'] + '\n'
        self.hide()
        self.redact = WindowRedact(self, result_text)
        self.redact.show()
