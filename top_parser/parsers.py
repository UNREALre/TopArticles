"""
All service parsers implemented in this module. Parser registration goes here too.

When adding new Source all we have to do is to implement two new classes: SourceParser and SourceParserBuilder.
Finally, we will need to register our newly created Parser within our Factory and we are done.
"""

import requests
import pickle
import os
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from fake_useragent import UserAgent

from .factory import ObjectFactory

app_dir = os.path.dirname(os.path.abspath(__file__))
useragent = UserAgent()
profile = webdriver.FirefoxProfile()


class HabrParser:
    def __init__(self, cookie_file):
        self.cookie_file = cookie_file

    def test_connection(self):
        auth_flag = False
        if os.path.exists(self.cookie_file):
            cookies = pickle.load(open(self.cookie_file, "rb"))
            for cookie in cookies:
                if cookie.get('name') == 'acc_sess_id':
                    auth_flag = True
                    break

        return auth_flag


class HabrParserBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, login, password, **kwargs):
        if not self._instance:
            cookie_file = self.authorize(login, password)
            self._instance = HabrParser(cookie_file)
        return self._instance

    def authorize(self, login, password):
        """
        Method authorize user within HabraHabr and return path to file with cookies.

        Receives user login and password. Generates random fake user agent.
        Using selenium authorizes user, retrieves cookies, stores them within pkl file.
        Returns full path to pkl file with cookies.

        :param login:
        :param password:
        :return: string:cookie_file
        """

        profile.set_preference('general.useragent.override', useragent.random)

        driver = webdriver.Firefox(profile)

        url = "https://account.habr.com/login/"
        driver.get(url)
        driver.find_element_by_id('email_field').send_keys(login)
        sleep(.5)
        driver.find_element_by_id('password_field').send_keys(password)
        sleep(1)
        driver.find_element_by_name('go').click()

        cookie_file = os.path.join(app_dir, 'tmp/habr_cookies_{}.pkl'.format(login))
        pickle.dump(driver.get_cookies(), open(cookie_file, 'wb'))

        driver.close()

        return cookie_file


class VcParser:
    def __init__(self, access_token):
        self.access_token = access_token

    def test_connection(self):
        pass


class VcParserBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, login, password, **kwargs):
        if not self._instance:
            access_token = self.authorize(login, password)
            self._instance = VcParser(access_token)
        return self._instance

    def authorize(self, login, password):
        return 'token'


factory = ObjectFactory()
factory.register_builder('HABR', HabrParserBuilder())
factory.register_builder('VC', VcParserBuilder())
