from PyQt6 import QtCore, QtGui, QtWidgets
import json
from models.getShopee import getShopee


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 90, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.txtLink = QtWidgets.QTextEdit(self.centralwidget)
        self.txtLink.setGeometry(QtCore.QRect(20, 140, 751, 301))
        self.txtLink.setObjectName("txtLink")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 10, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.btnProcess = QtWidgets.QPushButton(self.centralwidget)
        self.btnProcess.setGeometry(QtCore.QRect(670, 460, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnProcess.setFont(font)
        self.btnProcess.setObjectName("btnProcess")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Button Exec
        self.btnProcess.clicked.connect(self.scrappingProcess)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JuraganAR"))

        self.label.setText(_translate("MainWindow", "Shop ID"))
        self.label_2.setText(_translate("MainWindow", "JuraganAR"))
        self.btnProcess.setText(_translate(
            "MainWindow", self.read_setting("button_process")))
        self.txtLink.setPlaceholderText(_translate(
            "MainWindow", self.read_setting("placeholder_text")))

    def scrappingProcess(self):
        links = self.txtLink.toPlainText()
        if(links == ''):
            QtWidgets.QMessageBox.information(
                self.centralwidget, self.read_setting("message_box_title_info"), self.read_setting("message_box_message_info"))
        else:
            allLink = links.split("\n")
            errorLink = []
            for link in allLink:
                if(link == ''):
                    continue
                try:
                    getlink = []
                    shopees = getShopee(link)
                    numbers = shopees.getMaxPage()
                    getlink = shopees.getAllUrl(int(numbers))

                    if(self.read_allsetting('version') == "1.0"):
                        self.outputIt(getlink, link.replace(
                            'https://shopee.co.id/', '').replace('.', '_'))
                    else:
                        data = shopees.getAllData(getlink)

                        # Serializing json
                        json_object = json.dumps(data, indent=4)

                        # Writing to sample.json
                        with open("exports/"+self.read_allsetting('export_file_name')+"-"+link.replace('https://shopee.co.id/', '').replace('.', '_')+".json", "w") as outfile:
                            outfile.write(json_object)

                    # shopees.shutDown()

                except Exception as e:
                    print(e)
                    errorLink.append(link)
                    pass

            if(len(errorLink) > 0):
                QtWidgets.QMessageBox.warning(
                    self.centralwidget, self.read_setting('message_box_title_error'), self.read_setting('message_box_message_error')+"\n"+str(errorLink))

            QtWidgets.QMessageBox.information(
                self.centralwidget, self.read_setting('message_box_title_success'), self.read_setting('message_box_message_success'))

    def outputIt(self, links, shopid):
        textlinks = "'"+json.dumps(links)+"'"
        linku = textlinks.strip('[]')
        lastlink = "'"+linku+"'"

        lss = lastlink.replace('[', '').replace(']', '').replace('/', '')
        lsss = lss.replace('?', '.')
        lssss = lsss.replace('"', '').replace("'", "")
        text_file = open('exports/'+self.read_allsetting(
            'export_file_name')+'-'+shopid+'.txt', 'w')
        text_file.write(lssss)
        text_file.close()

    def read_setting(self, args):
        f = open("settings/settings.json")
        data = json.load(f)
        langs = data['lang']

        return data['lang_data'][langs][args]

    def read_allsetting(self, args):
        f = open("settings/settings.json")
        data = json.load(f)

        return data[args]


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
