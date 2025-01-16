import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from threads import AccountGeneratorThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'MainWindow.ui'), self)

        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.spinBox_2.valueChanged.connect(self.spinBox_2_valueChanged)
        self.spinBox_3.valueChanged.connect(self.spinBox_3_valueChanged)

        self._account_generator = None

    def spinBox_3_valueChanged(self, value: int):
        if self._account_generator:
            self._account_generator.proxy_change_threshold = value

    def spinBox_2_valueChanged(self, value: int):
        if self._account_generator:
            self._account_generator.timeout = value

    def pushButton_clicked(self):
        match self.pushButton.text():
            case 'Bắt đầu':
                self.pushButton.setText('Dừng')

                self._account_generator = AccountGeneratorThread()
                self._account_generator.threads = self.spinBox.value()
                self._account_generator.timeout = self.spinBox_2.value()
                self._account_generator.finished.connect(self._task_finished)
                self._account_generator.start()
            case 'Dừng':
                self.pushButton.setText('Dừng...')
                self._account_generator.stop = True

    def pushButton_2_clicked(self):
        path = os.path.join(os.getcwd(), 'output')
        os.makedirs(path, exist_ok=True)
        os.startfile(path)

    def _task_finished(self):
        self.pushButton.setText('Bắt đầu')
        QMessageBox.information(self, 'Thông báo', 'Đã dừng')
