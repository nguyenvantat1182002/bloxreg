import os
import time
import socket

from contextlib import closing
from datetime import datetime, timedelta
from typing import Optional
from DrissionPage import ChromiumPage, ChromiumOptions
from .account import Account
from .exceptions import ProxyError


def random_port(host: str = None):
    if not host:
        host = ''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
    

class Roblox:
    BROWSER_WIDTH = 520
    BROWSER_HEIGHT = 569

    def __init__(self, proxy: Optional[str] = None, browser_location: Optional[tuple] = None):
        options = ChromiumOptions()
        options.set_local_port(random_port())
        options.set_tmp_path(os.path.join(os.getcwd(), 'profiles'))
        options.set_pref('partition.default_zoom_level.x', -3.8017840169239308)
        options.set_pref('credentials_enable_service', False)
        options.no_imgs()

        if proxy:
            options.set_proxy(proxy)

        options.set_argument('--force-device-scale-factor', .75)
        options.set_argument('--high-dpi-support', .75)
        options.set_argument('--disable-features', 'PreloadMediaEngagementData,MediaPreloadExperimental')
        options.set_argument('--user-agent', 'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        
        self._page = ChromiumPage(addr_or_opts=options)
        self._page.set.window.size(Roblox.BROWSER_WIDTH + 16, Roblox.BROWSER_HEIGHT - 7)
        self._page.set.window.location(*(browser_location if browser_location else (0, 0)))

    @property
    def page(self) -> ChromiumPage:
        return self._page

    def signup(self, sigup_link: str, account: Optional[Account] = None, timeout: int = 30) -> Optional[Account]:
        if not account:
            account = Account.create_random()

        try:
            self._page.get(sigup_link, show_errmsg=True)
        except Exception:
            raise ProxyError
        
        time.sleep(3)

        for key, value in zip(('#MonthDropdown', '#DayDropdown', '#YearDropdown'), account.birthday):
            self._page.ele(key).select.by_value(value)
            time.sleep(.3)

        # for key, value in zip(('#signup-username', '#signup-password'), (account.username, account.password)):
        #     self._page.ele(key).input(value)
        #     time.sleep(.5)

        # self._page.ele('#MaleButton' if account.gender == 1 else '#FemaleButton').click()
        # time.sleep(1)

        time.sleep(2)

        try:
            self._page.ele('#signup-button').wait.enabled(timeout=5, raise_err=True).click()
        except Exception:
            return self.signup()
        
        end_time = datetime.now() + timedelta(seconds=timeout)
        while True:
            if datetime.now() > end_time:
                return None
            
            item = list(filter(lambda x: x['name'] == '.ROBLOSECURITY', self._page.cookies()))
            if item:
                account.security_token = item[-1]['value']
                break

            time.sleep(1)

        return account
