import pyautogui

from PyQt5.QtCore import QThread, QThreadPool, QRunnable, QReadWriteLock


class AccountGeneratorThread(QThread):
    def __init__(self):
        super().__init__()

        self._threads = 1
        self._timeout = 30
        self._proxy_change_threshold = 1
        self._stop = False
        self._rw_lock = QReadWriteLock()
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
    def proxy_change_threshold(self) -> int:
        return self._proxy_change_threshold

    @proxy_change_threshold.setter
    def proxy_change_threshold(self, value: int):
        self._proxy_change_threshold = value

    @property
    def stop(self) -> int:
        return self._stop

    @stop.setter
    def stop(self, value: int):
        self._stop = value

    @property
    def rw_lock(self) -> QReadWriteLock:
        return self._rw_lock

    def run(self):
        window_size = pyautogui.size()
        w_w, w_h = window_size.width, window_size.height
        b_w, b_h = 392, 429
        cols, rows = w_w // b_w, w_h // b_h
        
        for _ in range(self.threads):
            x = y = 0
            
            for _ in range(rows):
                for _ in range(cols):
                    item = AccountGeneratorRunnable(self, (x, y))
                    self._pool.start(item)

                    x += b_w

                    QThread.msleep(300)

                x = 0
                y += b_h

        self._pool.waitForDone()


class AccountGeneratorRunnable(QRunnable):
    def __init__(self, parent: AccountGeneratorThread, browser_location: tuple):
        super().__init__()

        self._parent = parent
        self._browser_location = browser_location

    def run(self):
        while not self._parent.stop:
            pass

