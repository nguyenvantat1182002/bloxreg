import os
import time

from datetime import datetime, timedelta
from typing import Optional
from DrissionPage import ChromiumPage, ChromiumOptions
from .account import Account
from .exceptions import ProxyError


class Roblox:
    def __init__(self, proxy: Optional[str] = None, browser_location: Optional[tuple] = None):
        options = ChromiumOptions().auto_port()
        options.set_tmp_path(os.path.join(os.getcwd(), 'profiles'))
        options.set_pref('partition.default_zoom_level.x', -3.8017840169239308)
        options.no_imgs()

        if proxy:
            options.set_proxy(proxy)

        options.set_argument('--force-device-scale-factor', .75)
        options.set_argument('--high-dpi-support', .75)
        
        self._page = ChromiumPage(addr_or_opts=options)
        self._page.set.window.size(520 + 16, 569 - 7)
        self._page.set.window.location(*(browser_location if browser_location else (0, 0)))

    @property
    def page(self) -> ChromiumPage:
        return self._page

    def signup(self, account: Optional[Account] = None, timeout: int = 30) -> Optional[Account]:
        if not account:
            account = Account.create_random()

        try:
            self._page.get('https://www.roblox.com/', show_errmsg=True)
        except Exception:
            raise ProxyError
        
        time.sleep(3)

        for key, value in zip(('#MonthDropdown', '#DayDropdown', '#YearDropdown'), account.birthday):
            self._page.ele(key).select.by_value(value)
            time.sleep(.8)

        for key, value in zip(('#signup-username', '#signup-password'), (account.username, account.password)):
            self._page.ele(key).input(value)
            time.sleep(1)

        self._page.ele('#MaleButton' if account.gender == 1 else '#FemaleButton').click()
        time.sleep(1)

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
    