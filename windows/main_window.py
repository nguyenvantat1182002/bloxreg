import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QTimer
from threads import AccountGeneratorThread
from datetime import datetime
from roblox import Account


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'MainWindow.ui'), self)

        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.spinBox_2.valueChanged.connect(self.spinBox_2_valueChanged)
        self.spinBox_3.valueChanged.connect(self.spinBox_3_valueChanged)

        self._account_generator = None
        self._start_time = datetime.now()
        self._title_update_timer = QTimer(self)
        self._title_update_timer.timeout.connect(self._update_window_title)

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
                self._account_generator.proxy_change_threshold = self.spinBox_3.value()
                self._account_generator.finished.connect(self._task_finished)
                self._account_generator.account_added_to_table.connect(self._add_account_to_table)
                self._account_generator.start()

                self._start_time = datetime.now()
                self._title_update_timer.start(1000)
            case 'Dừng':
                self.pushButton.setText('Dừng...')
                self._account_generator.stop = True
                self._title_update_timer.stop()

    def pushButton_2_clicked(self):
        path = os.path.join(os.getcwd(), 'output')
        os.makedirs(path, exist_ok=True)
        os.startfile(path)

    def _add_account_to_table(self, account: Account):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(account.username))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(account.password))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(account.security_token))

        self.tableWidget.scrollToBottom()

        self.label_3.setText(str(self.tableWidget.rowCount()))

    def _update_window_title(self):
        elapsed_time = datetime.now() - self._start_time
        hours, remainder = divmod(elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.setWindowTitle(f'BLOX REG | {hours:02}:{minutes:02}:{seconds:02}')

    def _task_finished(self):
        self.pushButton.setText('Bắt đầu')
        QMessageBox.information(self, 'Thông báo', 'Đã dừng')
