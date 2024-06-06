from __future__ import annotations

import random
import time
from typing import Any
from urllib.parse import quote
from urllib.request import getproxies

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from pixiv.utils import get_chromedriver

OptionsType = webdriver.chrome.options.Options

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
PROXIES = getproxies()


class PixivBrowser:
    def __init__(self, headless: bool = True):
        self.caps = DesiredCapabilities.CHROME.copy()
        self.caps["goog:loggingPrefs"] = {
            "performance": "ALL"
        }  # enable performance logs

        driver_path = get_chromedriver()
        self.__browser = webdriver.Chrome(
            service=Service(driver_path, ),
            options=self.__get_chrome_option(headless=headless),
            # desired_capabilities=self.caps,
        )
        self.__closed = False

    @staticmethod
    def __get_chrome_option(headless: bool) -> OptionsType:
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-browser-side-navigation")
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--user-agent=" + USER_AGENT)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

        if "all" in PROXIES:
            options.add_argument(f"--proxy-server={PROXIES['all']}")
        elif "https" in PROXIES:
            options.add_argument(f"--proxy-server={PROXIES['https']}")
        elif "http" in PROXIES:
            options.add_argument(f"--proxy-server={PROXIES['http']}")
        else:
            options.add_argument('--proxy-server="direct://"')
            options.add_argument("--proxy-bypass-list=*")

        return options

    def close(self):
        if not self.__closed:
            self.__browser.close()
            self.__closed = True

    def get_pixiv_cookie(self, username, password, slow_type: bool = True):
        redirect_url = 'https://www.pixiv.net/dashboard/works'
        login_url = f"https://accounts.pixiv.net/login?" \
                    f"return_to={quote(redirect_url)}&lang=zh_cn&source=pc&view_type=page"

        self.__browser.get(login_url)
        # time.sleep(60.0)

        username_element = self.__browser.find_element(
            By.XPATH, "// input [@ autocomplete ='username webauthn']")
        self.__type_content(username_element, username, slow=slow_type)

        self.__sleep_uniform(0.6, 1.5, slow=slow_type)

        password_element = self.__browser.find_element(
            By.XPATH, "// input [@ autocomplete ='current-password webauthn']")
        self.__type_content(password_element, password, slow=slow_type)
        self.__sleep_uniform(0.4, 0.8, slow=slow_type)

        password_element.send_keys(Keys.ENTER)
        # label_selectors = [f"contains(text(), '{label}')" for label in ["ログイン", "Log In", "登录", "로그인", "登入"]]
        # el = self.__browser.find_element(By.XPATH, f"//button[@type='submit'][{' or '.join(label_selectors)}]")
        # el.click()
        # self.__browser.find_element(By.XPATH, "// button [@ type ='submit']").click()

        for _ in range(180):
            if self.__browser.current_url[: len(redirect_url)] == redirect_url:
                break
            time.sleep(1.0)
        else:
            self.close()
            raise ValueError('Login failed.')

        items = sorted([(item['name'], item['value'])
                        for item in self.__browser.get_cookies()
                        if item['domain'].endswith('.pixiv.net')])
        raw_items = [
            item for item in self.__browser.get_cookies()
            if item['domain'].endswith('.pixiv.net')
        ]
        return {key: value for key, value in items}, raw_items

    @staticmethod
    def __sleep_uniform(min_sleep: float, max_sleep: float, slow: bool = True) -> None:
        if slow:
            time.sleep(random.uniform(min_sleep, max_sleep))

    @staticmethod
    def __type_content(elm: Any, text: str, slow: bool = False) -> None:
        if slow:
            for character in text:
                elm.send_keys(character)
                time.sleep(random.uniform(0.3, 0.7))
        else:
            elm.send_keys(text)
