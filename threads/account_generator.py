import pyautogui
import requests
import os
import queue
import random

from roblox import Roblox, ProxyError, Account
from PyQt5.QtCore import QThread, QThreadPool, QRunnable, QReadWriteLock, QMutex, QMutexLocker, pyqtSignal


def get_proxy(count: int = 1) -> queue.Queue[str]:
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


def get_signup_links() -> queue.Queue[Account]:
    q = queue.Queue()
    file_path = os.path.join(os.getcwd(), 'signup_links.txt')

    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.read().splitlines()
        file.truncate(0)
        
    for line in lines:
        email, password, signup_link = line.split('|')
        item = Account.create_random()
        item.email = email
        item.email_password = password
        item.signup_link = signup_link
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
        self._proxies: queue.Queue[str] = queue.Queue()
        self._signup_links: queue.Queue[Account] = queue.Queue()
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

    @property
    def signup_links(self) -> queue.Queue[Account]:
        return self._signup_links
    
    @signup_links.setter
    def signup_links(self, value: queue.Queue[Account]):
        self._signup_links = value

    def run(self):
        window_size = pyautogui.size()
        w_w, w_h = window_size.width, window_size.height
        b_w, b_h = 392, 429
        cols, rows = w_w // b_w, w_h // b_h
        created_threads = 0

        self._proxies = get_proxy(self.threads)
        self._signup_links = get_signup_links()

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
        proxy = None

        while not self._parent.stop:
            with QMutexLocker(self._parent.mutex):
                if self._parent.signup_links.empty():
                    self._parent.signup_links = get_signup_links()
                    continue
                
                account = self._parent.signup_links.get_nowait()

                if (self._current_reg_count % self._parent.proxy_change_threshold == 0) or self._should_change_proxy:
                    if self._parent.proxies.empty() or self._should_change_proxy:
                        self._parent.proxies = get_proxy(self._parent.threads)

                    if self._should_change_proxy:
                        self._should_change_proxy = False
                    
                    proxy = self._parent.proxies.get_nowait()

                print(proxy)
                
                rblx = Roblox(proxy, self._browser_location)
                
            try:
                result = rblx.signup(account.signup_link, timeout=self._parent.timeout)
                # result = rblx.signup(timeout=self._parent.timeout)
            
                if result is not None:
                    self._parent.rw_lock.lockForWrite()
                    account.username = result.username
                    result.security_token = result.security_token
                    result.save()
                    self._parent.account_added_to_table.emit(result)
                    self._parent.account_added_to_table.emit(account)
                    self._parent.rw_lock.unlock()
                else:
                    with QMutexLocker(self._parent.mutex):
                        self._parent.signup_links.put_nowait(account)
            except (ProxyError, Exception) as ex:
                ex_name = type(ex).__name__

                if ex_name == 'ProxyError':
                    self._should_change_proxy = True
                
                if not ex_name == 'LinkAlreadyUsedError':
                    with QMutexLocker(self._parent.mutex):
                        self._parent.signup_links.put_nowait(account)
            finally:
                with QMutexLocker(self._parent.mutex):
                    try:
                        rblx.close()
                    except Exception:
                        pass

            self._current_reg_count += 1
            