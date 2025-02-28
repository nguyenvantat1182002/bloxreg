import qdarkstyle

from windows import MainWindow
from PyQt5.QtWidgets import QApplication


palette = qdarkstyle.DarkPalette()
palette.ID = 'light'

app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=palette))

win = MainWindow()
win.show()

app.exec_()
