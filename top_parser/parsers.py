# -*- coding: utf-8 -*-
"""
All service parsers implemented in this module. Parser registration goes here too.

When adding new Source all we have to do is to implement two new classes: SourceParser and SourceParserBuilder.
Finally, we will need to register our newly created Parser within our Factory and we are done.
"""

import requests
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
        pages_with_arts = pages_with_arts[:3]  # for fast debug
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
        Method authorize user within HabraHabr and return selenium driver object with all required cookies.

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
    """Parse for VC.RU resource."""

    def __init__(self, driver):
        self.driver = driver

    def test_connection(self):
        """Test if authentication to source with user credentials went fine."""

        auth_flag = False
        if self.driver.get_cookies():
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie.get('name') == 'osnova-aid':
                    auth_flag = True
                    break

        return auth_flag

    def do_parse(self, url):
        """Starts parsing process"""
        sleep(1)

        height = self.driver.execute_script("return document.body.scrollHeight")
        # Simulation of scrolling down process, until all articles will be shown
        while True:
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.END)

            sleep(3)  # wait till new articles will be loaded via AJAX

            current_height = self.driver.execute_script("return document.body.scrollHeight")
            if current_height != height:
                height = current_height
            else:
                # no more articles to load
                break

        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')
        articles = soup.find_all('div', {'class': 'feed__item l-island-round'})

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            page_articles = executor.map(self.parse_article, articles)

        self.driver.close()

        return page_articles

    def parse_article(self, article):
        """Receives article preview. Return dict with fill article info, or with existed article in db."""

        parsed_article = dict()

        author = article.find('div', {'class': 'content-header-author__name'})
        if author and author.get_text().strip() != "Промо":  # we don't want promo blocks to get parsed
            h2 = article.find('h2')
            full_link = article.find('a', {'class': 'content-feed__link'})
            href = full_link['href'] if full_link else ''

            if href:
                try:
                    article = Article.objects.get(url=href)
                except Article.DoesNotExist:
                    article = None

                if not article:
                    try:
                        detail = BeautifulSoup(requests.get(href).content, "lxml")
                        body_post = detail.find('div', {'class': 'content content--full'})
                        if body_post:
                            # remove some web page stuff
                            try:
                                body_post.find('div', {'class': 'l-island-a l-mv-20 content-counters'}).decompose()
                                body_post.find('div', {'class': 'authorCard l-mt-30'}).decompose()
                            except Exception as ex:
                                logger.error('Error "{}" while trying to remove unused elements from page: {}'.format(ex, href))
                            full_text = body_post.get_text().strip()
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


class VcParserBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, login, password, **kwargs):
        driver = self.authorize(login, password)
        return VcParser(driver)

    def authorize(self, login, password):
        """
        Method authorize user within VC and return selenium driver object with all required cookies.

        Receives user login and password. Generates random fake user agent.
        Using selenium authorizes user, retrieves cookies.
        Returns selenium web driver object for next actions.

        :param login:
        :param password:
        :return: webdriver:driver
        """

        profile.set_preference('general.useragent.override', useragent.random)

        driver = webdriver.Firefox(profile)

        try:
            url = "https://vc.ru/"
            driver.get(url)
            driver.find_element_by_class_name('site-header-user-login__label').click()
            auth_buttons = driver.find_elements_by_class_name('social-auth__button')
            for button in auth_buttons:
                if button.get_attribute('air-click') == 'auth_goto_tab':
                    button.click()
                    break
            driver.find_element_by_name('login').send_keys(login)
            sleep(.5)
            driver.find_element_by_name('password').send_keys(password)
            sleep(1)
            driver.find_element_by_name('password').send_keys(Keys.ENTER)
        except Exception as ex:
            logger.error('Error during auth process VC.RU: {}'.format(ex))

        return driver


factory = ObjectFactory()
factory.register_builder('HABR', HabrParserBuilder())
factory.register_builder('VC', VcParserBuilder())
