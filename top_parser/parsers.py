"""
All service parsers implemented in this module. Parser registration goes here too.

When adding new Source all we have to do is to implement two new classes: SourceParser and SourceParserBuilder.
Finally, we will need to register our newly created Parser within our Factory and we are done.
"""

import requests
import pickle
import logging
import os
import concurrent.futures
import itertools
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

from .factory import ObjectFactory
from article.models import Article

logger = logging.getLogger('django')

app_dir = os.path.dirname(os.path.abspath(__file__))
useragent = UserAgent()
profile = webdriver.FirefoxProfile()


class HabrParser:
    """Parser for HabraHabr resource."""

    def __init__(self, driver):
        self.driver = driver

    def test_connection(self):
        """Test if authentication to source with user credentials went fine."""

        auth_flag = False
        if self.driver.get_cookies():
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie.get('name') == 'acc_sess_id':
                    auth_flag = True
                    break

        return auth_flag

    def do_parse(self, url):
        """Start parsing process. Get pages to parse. Return generator with parsed articles"""

        sleep(1)
        feed_url = 'https://habr.com/ru/conversations/'
        # we have to visit some light-weight page before going to feed to prevent redirect
        self.driver.get(feed_url)

        sleep(1)
        feed_url = 'https://habr.com/ru/feed/'
        self.driver.get(feed_url)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        paginator = soup.find('ul', id='nav-pagess')
        pages_with_arts = ['https://habr.com/ru/feed/page1/']  # list of pages to be iterated through
        if paginator:
            lis = [li for li in paginator.find_all('li')]
            last_li_href = lis[-1].find('a')['href']
            last_page = int(last_li_href.split('/')[-2].split('page')[-1])

            for i in range(2, last_page + 1):
                pages_with_arts.append('https://habr.com/ru/feed/page{}/'.format(i))

        # TODO: implement multithreading. We need separate driver (?) for each thread to work properly within selenium
        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #    articles = executor.map(self.parse_page, pages_with_arts)

        articles = list()
        for page in pages_with_arts:
            articles.append(self.parse_page(page))

        self.driver.close()

        return list(itertools.chain(*articles))

    def parse_page(self, page):
        """Receives page url to parse articles from. Returns list of articles."""
        sleep(1)

        self.driver.get(page)
        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')
        articles = soup.find_all('article')

        page_articles = list()
        if articles:
            # attempt to speed up the process while main threading doesn't work in current selenium realization
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                page_articles = executor.map(self.parse_article, articles)

        return page_articles

    def parse_article(self, article):
        parsed_article = dict()
        h2 = article.find('h2')
        h2_a = article.find('h2').find('a')
        href = h2_a['href'] if h2_a else ''

        if href:
            try:
                article = Article.objects.get(url=href)
            except Article.DoesNotExist:
                article = None

            if not article:
                try:
                    detail = BeautifulSoup(requests.get(href).content, "lxml")
                    body_post = detail.find('div', id='post-content-body')
                    if body_post:
                        full_text = detail.find('div', id='post-content-body').get_text().strip()
                        parsed_article = {
                            'url': href,
                            'header': h2.get_text().strip(),
                            'text': full_text
                        }
                        sleep(0.5)
                    else:
                        logging.error("URL {} has no body.".format(href))
                except Exception as ex:
                    logger.error('Error "{}" while trying to open url: {}'.format(ex, href))
            else:
                # we have already stored this article in database and just need to connect it with user
                parsed_article = {
                    'db_article': article
                }

        return parsed_article


class HabrParserBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, login, password, **kwargs):
        driver = self.authorize(login, password)
        return HabrParser(driver)

    def authorize(self, login, password):
        """
        Method authorize user within HabraHabr and return path to file with cookies.

        Receives user login and password. Generates random fake user agent.
        Using selenium authorizes user, retrieves cookies.
        Returns selenium web driver object for next actions.

        :param login:
        :param password:
        :return: webdriver:driver
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

        return driver


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
