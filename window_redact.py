from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import pandas as pd
import stanza
import pymorphy3
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
import script_for_graph
import importlib
from window_view import WindowView
from datetime import datetime

importlib.reload(script_for_graph)


class WindowRedact(QMainWindow):
    def __init__(self, parent, txt_content):
        super(WindowRedact, self).__init__(parent)
        self.setupUi(self)
        self.view_graph = None
        self.avg_rate = None
        self.textEdit.setText(txt_content)
        self.pushButton.clicked.connect(self.build_graph)

    def load_stop_words(self):
        stopwords = []
        path_to_file = "Stopwords.txt"
        with open(path_to_file, "r", encoding="utf-8") as fl:
            for line in fl:
                stopwords.append(line.strip("\n"))
        return stopwords

    def norm_form(self, morph, word):
        return morph.parse(word)[0].normal_form

    def build_graph(self):
        self.textEdit.setReadOnly(True)
        message = f"Подключение библиотек..."
        self.statusbar.showMessage(message)
        sents = self.txt_prepare()
        triplets = self.get_triplets(sents)
        for_df = self.clear_triplet(triplets)
        df_filtered = self.df_prepare(for_df)
        nodes, df_for_draw = self.split_data(df_filtered)
        info_dict, label_dict, sent_string = self.process_edges(nodes, df_for_draw)
        name = self.visualize_graph(nodes, info_dict, label_dict)
        dts = datetime.now().strftime("%d%m%Y_%H%M%S")
        sents_save = f"Sample_sents_{dts}.txt"
        with open(sents_save, "w", encoding="utf-8") as f:
            f.write(sent_string)
        print('GG EZ', '\n')
        self.hide()
        self.view_graph = WindowView(self, name)
        self.view_graph.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(66, 72, 116);\n"
                                 "color: rgb(244, 238, 255);\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton.setStyleSheet("font: 12pt \"Cambria\";\n"
                                      "color: rgb(0, 0, 0);\n"
                                      "background-color: rgb(244, 238, 255);\n"
                                      "border-radius: 10%")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(188, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setStyleSheet("font: 12pt \"Cambria\";\n"
                                       "color: rgb(244, 238, 255)")
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setStyleSheet("font: 12pt \"Cambria\";\n"
                                    "background-color: rgb(244, 238, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "border-radius: 10%")
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Изменение текста"))
        self.pushButton.setText(_translate("MainWindow", "Построить граф"))

    def close_and_return(self):
        self.close()
        self.parent().show()

    def txt_prepare(self):
        # Обработка текста из txt-файла
        txt_content_replaced = self.textEdit.toPlainText().replace('\n', ' ')
        sentences1 = sent_tokenize(txt_content_replaced, language="russian")
        long_sents1 = [i for i in sentences1 if len(i) > 20]
        return long_sents1

    def get_triplets(self, long_sents):
        # инициализация пайплайна
        nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma,ner,depparse', use_gpu = True,\
                              download_method=stanza.DownloadMethod.NONE)
        # формирование триплетов
        triplets = []
        t = tqdm(long_sents)
        for s in t:
            self.show_progress(t)
            doc = nlp(s)
            for sent in doc.sentences:
                entities = [ent.text for ent in sent.ents]
                res_d = dict()
                temp_d = dict()
                for word in sent.words:
                    temp_d[word.text] = {"head": sent.words[word.head - 1].text, "dep": word.deprel, "id": word.id}
                for k in temp_d.keys():
                    nmod_1 = ""
                    nmod_2 = ""
                    if (temp_d[k]["dep"] in ["nsubj", "nsubj:pass"]) & (k in entities):
                        res_d[k] = {"head": temp_d[k]["head"]}

                        for k_0 in temp_d.keys():
                            if (temp_d[k_0]["dep"] in ["obj", "obl"]) & \
                                    (temp_d[k_0]["head"] == res_d[k]["head"]) & \
                                    (temp_d[k_0]["id"] > temp_d[res_d[k]["head"]]["id"]):
                                res_d[k]["obj"] = k_0
                                break

                        for k_1 in temp_d.keys():
                            if (temp_d[k_1]["head"] == res_d[k]["head"]) & (k_1 == "не"):
                                res_d[k]["head"] = "не " + res_d[k]["head"]

                        if "obj" in res_d[k].keys():
                            for k_4 in temp_d.keys():
                                if (temp_d[k_4]["dep"] == "nmod") & \
                                        (temp_d[k_4]["head"] == res_d[k]["obj"]):
                                    nmod_1 = k_4
                                    break

                            for k_5 in temp_d.keys():
                                if (temp_d[k_5]["dep"] == "nummod") & \
                                        (temp_d[k_5]["head"] == nmod_1):
                                    nmod_2 = k_5
                                    break
                            res_d[k]["obj"] = res_d[k]["obj"] + " " + nmod_2 + " " + nmod_1

                if len(res_d) > 0:
                    triplets.append([s, res_d])
        self.show_progress(t, last=True)
        return triplets

    def show_progress(self, t, last=False):
        progress_dict = t.format_dict
        percentage = progress_dict['n'] / progress_dict['total'] * 100
        self.progressBar.setValue(int(percentage))
        progress = str(t)
        time_val = progress.split('[')[-1].split(',')[0]
        rate = progress.split('[')[-1].split(',')[-1].split('i')[0]
        elapsed = time_val.split('<')[0]
        remaining = time_val.split('<')[-1]
        if last:
            rate = self.avg_rate
        else:
            self.avg_rate = rate
        message = f"Обработка элемента: {progress_dict['n']}   Всего: {progress_dict['total']}\
    Частота: {rate} ед/с   Времени прошло: {elapsed}   Времени осталось: {remaining}"
        self.statusbar.showMessage(message)

    def clear_triplet(self, triplets):
        # очистка триплетов
        clear_text = lambda x: "".join(i if (i.isdigit()) | (i.isalpha()) | (i in [" "]) else " " for i in x )
        clear_triplets = dict()
        for tr in triplets:
            for k in tr[1].keys():
                if "obj" in tr[1][k].keys():
                    ## clear_text убрать, если не нужна очистка предложений
                    clear_triplets[clear_text(tr[0])] = [k, tr[1][k]['head'], tr[1][k]['obj']]

        for_df = []
        for k in clear_triplets.keys():
            for_df.append([k]+clear_triplets[k])
        return for_df

    def df_prepare(self, for_df):
        #подготовка датафрейма
        morph = pymorphy3.MorphAnalyzer(lang="ru")
        stopwords = self.load_stop_words()
        df_triplets = pd.DataFrame(for_df, columns=["full_sent", "subject", "verb", "object"])
        df_triplets["subj_n_f"] = df_triplets["subject"].apply(lambda x: self.norm_form(morph, x))
        df_triplets["obj_n_f"] = df_triplets["object"].apply(lambda x: self.norm_form(morph, x))
        df_filtered = df_triplets[(~df_triplets["subj_n_f"].isin(stopwords)) &\
                                  (~df_triplets["obj_n_f"].isin(stopwords))].sort_values(by="obj_n_f", ascending=False,\
                                                                                         ignore_index=True)
        return df_filtered

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def split_data(self, df_filtered):
        #разделение данных на блоки
        groups = list(self.chunks(df_filtered["obj_n_f"].unique(), 100))
        gr_num = 0
        df_for_draw = df_filtered[df_filtered["obj_n_f"].isin(groups[gr_num])]
        nodes = pd.unique(df_for_draw[["subj_n_f", "obj_n_f"]].values.ravel("K"))
        return nodes, df_for_draw

    def process_edges(self, nodes, df_for_draw):
        #обработка данных о связях
        df_d_d = df_for_draw.drop_duplicates(subset=["subj_n_f", "obj_n_f", "verb"])[["subj_n_f", "obj_n_f", "verb",\
                                                                                      "full_sent"]]
        info_dict = dict()
        label_dict = dict()
        sent_string = ''
        for cc, raw in enumerate(df_d_d.values):
            info_dict[(raw[0], raw[1])] = {f"sent_{cc}": raw[3]}
            sent_string = sent_string + raw[3][:-1] + '.' + '\n'
            label_dict[(raw[0], raw[1])] = raw[2]
        return info_dict, label_dict, sent_string

    def visualize_graph(self, nodes, info_dict, label_dict, gr_num=0):
        # визуализация графа
        word_num = dict()
        header = script_for_graph.header_text
        tail = script_for_graph.tail_text
        for c, word in enumerate(nodes):
            word_num[word] = c + 1
        header += """\nvar nodes = new vis.DataSet([\n"""
        for w in nodes:
            header += "{"
            header += f"""         id: {word_num[w]},
                                        label: "{w}"\n"""
            header += "},"
        header += "   ]);\n"

        header += """var edges = new vis.DataSet(["""
        for k in info_dict.keys():
            header += "{"
            header += f"""       from: {word_num[k[0]]},
                            to: {word_num[k[1]]},
                            arrows: "to",
                            label: "{label_dict[k]}",
                            info: {info_dict[k]}\n"""
            header +="},"
        header += "   ]);\n"

        full_text = ""
        full_text += header
        full_text += tail
        dt = datetime.now().strftime("%d%m%Y_%H%M%S")
        name = f"Graph_for_group_{gr_num} {dt}.html"
        with open(name, "w", encoding="utf-8") as f:
            f.write(full_text)
        return name