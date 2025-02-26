import os
import time
import socket

from bs4 import BeautifulSoup
from contextlib import closing
from datetime import datetime, timedelta
from typing import Optional
from DrissionPage import ChromiumPage, ChromiumOptions
from .account import Account
from .exceptions import ProxyError, LinkAlreadyUsedError


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

    def __init__(self, proxy: str, browser_location: Optional[tuple] = None):
        options = ChromiumOptions()

        options.set_proxy(proxy)
        options.no_imgs()

        port = random_port()
        options.set_local_port(port)
        options.set_user_data_path(os.path.join(os.getcwd(), 'profiles', str(port)))

        options.set_pref('partition.default_zoom_level.x', -3.8017840169239308)
        options.set_pref('credentials_enable_service', False)
        
        options.set_argument('--force-device-scale-factor', .75)
        options.set_argument('--high-dpi-support', .75)
        options.set_argument('--disable-features', 'PreloadMediaEngagementData,MediaPreloadExperimental')
        options.set_user_agent('Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.3')
        
        self._page = ChromiumPage(addr_or_opts=options)
        self._page.set.window.size(Roblox.BROWSER_WIDTH + 16, Roblox.BROWSER_HEIGHT - 7)
        self._page.set.window.location(*(browser_location if browser_location else (0, 0)))
        
    def close(self):
        self._page.quit(del_data=True)

    def signup(self, sigup_link: str, account: Optional[Account] = None, timeout: int = 30) -> Optional[Account]:
        if not account:
            account = Account.create_random()

        try:
            self._page.get(sigup_link, show_errmsg=True)
        except Exception:
            raise ProxyError
        
        for key, value in zip(('#MonthDropdown', '#DayDropdown', '#YearDropdown'), account.birthday):
            self._page.ele(key).select.by_value(value)
            
        try:
            self._page.ele('#signup-button').wait.enabled(timeout=10, raise_err=True).click()
        except Exception:
            return self.signup(sigup_link)
        
        end_time = datetime.now() + timedelta(seconds=timeout)
        while True:
            item = list(filter(lambda x: x['name'] == '.ROBLOSECURITY', self._page.cookies()))
            if item:
                soup = BeautifulSoup(self._page.html, 'html.parser')
                account.username = soup.select_one('meta[name="user-data"]')['data-name']
                account.security_token = item[-1]['value']
                break

            if 'Invalid link' in self._page.html:
                raise LinkAlreadyUsedError

            iframe = self._page('css:iframe[id="arkose-iframe"]', timeout=3)
            if iframe and {'height', 'width'}.issubset(iframe.attrs):
                return None
                
            if datetime.now() > end_time:
                return None

            time.sleep(1)

        return account
