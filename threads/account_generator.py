import pyautogui
import os

from PyQt5.QtCore import QThread, QThreadPool, QRunnable
from roblox import Roblox


class AccountGeneratorThread(QThread):
    def __init__(self):
        super().__init__()

        self._threads = 1
        self._timeout = 30
        self._stop = False
        self._pool = QThreadPool()
        self._pool.setMaxThreadCount(9999)

    @property
    def threads(self) -> int:
        return self._threads
    
    @threads.setter
    def threads(self, value: int):
        self._threads = value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value

    @property
    def stop(self) -> int:
        return self._stop

    @stop.setter
    def stop(self, value: int):
        self._stop = value

    def run(self):
        window_size = pyautogui.size()
        w_w, w_h = window_size.width, window_size.height
        cols, rows = w_w // Roblox.BROWSER_HEIGHT, w_h // Roblox.BROWSER_WIDTH
        print(cols, rows)
