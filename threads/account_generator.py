import pyautogui
import requests
import os
import queue
import random

from roblox import Roblox, ProxyError
from PyQt5.QtCore import QThread, QThreadPool, QRunnable, QReadWriteLock, QMutex, QMutexLocker, pyqtSignal


def get_proxy(count: int = 1) -> queue.Queue:
    with open(os.path.join(os.getcwd(), 'API_Links.txt'), encoding='utf-8') as file:
        api_links = file.read().strip().splitlines()

    api_link = random.choice(api_links)
    api_link = api_link.replace('num=1', f'num={count}')

    response = requests.get(api_link)

    items = response.text.strip().splitlines()
    q = queue.Queue()
    
    for item in items:
        q.put_nowait(item)

    return q


class AccountGeneratorThread(QThread):
    account_added_to_table = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self._threads = 1
        self._timeout = 30
        self._proxy_change_threshold = 1
        self._stop = False
        self._rw_lock = QReadWriteLock()
        self._mutex = QMutex()
        self._proxies = queue.Queue()
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
    
    @property
    def mutex(self) -> QMutex:
        return self._mutex
    
    @property
    def proxies(self) -> queue.Queue[str]:
        return self._proxies
    
    @proxies.setter
    def proxies(self, value: queue.Queue[str]):
        self._proxies = value

    def run(self):
        window_size = pyautogui.size()
        w_w, w_h = window_size.width, window_size.height
        b_w, b_h = 392, 429
        cols, rows = w_w // b_w, w_h // b_h
        created_threads = 0

        self._proxies = get_proxy(self.threads)

        for _ in range(self.threads):
            x = y = 0

            for _ in range(rows):
                for _ in range(cols):
                    if created_threads >= self.threads:
                        break

                    item = AccountGeneratorRunnable(self, (x, y))
                    self._pool.start(item)

                    x += Roblox.BROWSER_WIDTH - 16
                    created_threads += 1

                    QThread.msleep(300)

                x = 0
                y += Roblox.BROWSER_HEIGHT

        self._pool.waitForDone()


class AccountGeneratorRunnable(QRunnable):
    def __init__(self, parent: AccountGeneratorThread, browser_location: tuple):
        super().__init__()

        self._parent = parent
        self._browser_location = browser_location
        self._current_reg_count = 0
        self._should_change_proxy = False

    def run(self):
        with QMutexLocker(self._parent.mutex):
            proxy = self._parent.proxies.get_nowait()

        while not self._parent.stop:
            with QMutexLocker(self._parent.mutex):
                if (not self._current_reg_count == 0 and self._current_reg_count % self._parent.proxy_change_threshold == 0) or self._should_change_proxy:
                    if self._parent.proxies.empty() or self._should_change_proxy:
                        self._parent.proxies = get_proxy(self._parent.threads)

                    if self._should_change_proxy:
                        self._should_change_proxy = False
                    
                    QThread.msleep(5000 if self._parent.proxy_change_threshold < 2 else 3000)

                    proxy = self._parent.proxies.get_nowait()

            try:
                with QMutexLocker(self._parent.mutex):
                    rblx = Roblox(proxy, self._browser_location)

                try:
                    acc = rblx.signup(timeout=self._parent.timeout)
                    if acc is not None:
                        self._parent.rw_lock.lockForWrite()
                        acc.save()
                        self._parent.account_added_to_table.emit(acc)
                        self._parent.rw_lock.unlock()
                except ProxyError:
                    self._should_change_proxy = True
                except Exception as ex:
                    print(ex)
                finally:
                    with QMutexLocker(self._parent.mutex):
                        try:
                            rblx.page.quit(timeout=10, del_data=True)
                        except Exception:
                            pass
            except Exception as ex:
                print(ex)

            self._current_reg_count += 1
            