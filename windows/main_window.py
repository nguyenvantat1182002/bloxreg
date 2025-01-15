import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'MainWindow.ui'), self)

        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)

    def pushButton_clicked(self):
        match self.pushButton.text():
            case 'Bắt đầu':
                self.pushButton.setText('Dừng')
            case 'Dừng':
                self.pushButton.setText('Bắt đầu')

    def pushButton_2_clicked(self):
        path = os.path.join(os.getcwd(), 'output')
        os.makedirs(path, exist_ok=True)
        os.startfile(path)
