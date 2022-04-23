from Interface import Ui_MainWindow as View
from PyQt6 import QtWidgets, QtCore, QtGui
import requests, json, sys

class CryptoData(View):
    def __init__(self, window):
        self.setupUi(window)
        self.PageStart = 1
        self.PageListSize = 30
        self.CryptoPage = []
        self.Next.clicked.connect(self.NextPage)
        self.Back.clicked.connect(self.PrevPage)
        self.Filter.textEdited.connect(self.FindCrypto)
        self.CryptoPage = self.PullJsonData(self.PageStart, self.PageListSize)['data']['cryptoCurrencyList']
        self.filter = ""
        self.LoadPage(self.filter)
        
    def PullJsonData(self, start, count):
        url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start={0}&limit={1}&sortBy=market_cap' \
            '&sortType=desc&cryptoType=all&tagType=all&audited=false'.format(start, count)

        jsonString = requests.get(url)
        if jsonString.status_code != 200:
            raise Exception("Сервер недоступен")
        jsonObj = json.loads(jsonString.text)
        if jsonObj['status']['error_code'] != '0':
            raise Exception("Некорректные входные данные")
        return jsonObj

    def FindCrypto(self):
        self.filter = self.Filter.text().lower()
        self.LoadPage(self.filter)

    def NextPage(self):
        self.PageStart += self.PageListSize
        self.CryptoPage = self.PullJsonData(self.PageStart, self.PageListSize)['data']['cryptoCurrencyList']
        self.LoadPage(self.filter)

    def PrevPage(self):
        if self.PageStart != 1:
            self.PageStart -= self.PageListSize
            self.CryptoPage = self.PullJsonData(self.PageStart, self.PageListSize)['data']['cryptoCurrencyList']
            self.LoadPage(self.filter)

    def CustomPercent(self, item, percentName):
        percent = round(item['quotes'][0][percentName], 2)
        if round(item['quotes'][0][percentName], 2) < 0:
            return "▼ " + str(percent) + "%"
        else:
            return "▲ " + str(percent) + "%"

    def FindAccuracy(self, item):
        if  item['quotes'][0]['price'] < 0.01:
            return "{:.10f}".format(float(item['quotes'][0]['price']))
        return round(item['quotes'][0]['price'], 2)

    def LoadPage(self, substr):
        _translate = QtCore.QCoreApplication.translate

        if substr != "":
            for i in reversed(range(self.gridLayout_2.count())): 
                self.gridLayout_2.itemAt(i).widget().deleteLater()

        i = 0
        for key in self.CryptoPage:
            if substr != "" and key['name'].lower().find(substr) == -1 and key['symbol'].lower().find(substr) == -1:
                continue

            self.N = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.N.sizePolicy().hasHeightForWidth())
            self.N.setSizePolicy(sizePolicy)
            self.N.setMinimumSize(QtCore.QSize(0, 0))
            font = QtGui.QFont()
            font.setPointSize(16)
            self.N.setFont(font)
            self.N.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.N.setObjectName("N" + str(i))
            self.N.setStyleSheet("color: #edff21;")
            self.gridLayout_2.addWidget(self.N, i, 0, 1, 1)
            self.MC = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            font = QtGui.QFont()
            font.setPointSize(16)
            self.MC.setFont(font)
            self.MC.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.MC.setObjectName("MC" + str(i))
            self.gridLayout_2.addWidget(self.MC, i, 4, 1, 1)
            self.H24 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            font = QtGui.QFont()
            font.setPointSize(16)
            self.H24.setFont(font)
            self.H24.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.H24.setObjectName("H24" + str(i))

            if round(key['quotes'][0]['percentChange24h'], 2) < 0:
                self.H24.setStyleSheet("color: #ff2400;")
            else:
                self.H24.setStyleSheet("color: #32cd32;")

            self.gridLayout_2.addWidget(self.H24, i, 2, 1, 1)
            self.P = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            font = QtGui.QFont()
            font.setPointSize(16)
            self.P.setFont(font)
            self.P.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.P.setObjectName("P" + str(i))
            self.gridLayout_2.addWidget(self.P, i, 1, 1, 1)
            self.D7 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
            font = QtGui.QFont()
            font.setPointSize(16)
            self.D7.setFont(font)
            self.D7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.D7.setObjectName("D7" + str(i))

            if round(key['quotes'][0]['percentChange7d'], 2) < 0:
                 self.D7.setStyleSheet("color: #ff2400;")
            else:
                self.D7.setStyleSheet("color: #32cd32;")

            self.gridLayout_2.addWidget(self.D7, i, 3, 1, 1)

            self.N.setText(_translate("MainWindow", key['name'] + " " + '(' + key['symbol'] + ')'))
            self.MC.setText(_translate("MainWindow", "$" + format(round(key['quotes'][0]['marketCap']), ',')))
            price = self.FindAccuracy(key)
            if type(price) != str:
                price = format(price, ',')

            self.P.setText(_translate("MainWindow", "$" + price))
            self.H24.setText(_translate("MainWindow", self.CustomPercent(key, 'percentChange24h')))
            self.D7.setText(_translate("MainWindow", self.CustomPercent(key, 'percentChange7d')))
            i += 1

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    view = CryptoData(window)
    window.show()
    sys.exit(app.exec())