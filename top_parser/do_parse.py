# -*- coding: utf-8 -*-
"""
Main parsing process goes here.

Module defines two base methods: start_process() and save_to_db()

start_process() method walks through every user source in the system and fires appropriate feed parsers. At the end,
method gets the list of parsed articles. This list passes to save_to_db() method.

save_to_db() method receives parsed articles, walks through every article and check if article exists in DB?
If article exists, method just ensures that article is linked with subscribed user.
If there is no such article, method will add it to DB.
"""

import logging
import top_parser.parsers as top_parser
from top_news.helpers import AESCipher

from user.models import UserSource
from article.models import Article

logger = logging.getLogger('django')


def start_process():
    """Fires parsing process."""

    user_sources = UserSource.objects.all()
    for user_source in user_sources:
        auth_data = {
            'login': user_source.login,
            'password': AESCipher(user_source.password, user_source.user.password).decrypt()
        }

        parser = top_parser.factory.create(user_source.source.label, **auth_data)
        if parser and parser.test_connection():
            logger.info('Successfully connected to source {} for user {}'.format(
                user_source.source.label, user_source.user.username))

            articles = parser.do_parse(user_source.source.feed_url)
            save_to_db(articles, user_source)
        else:
            logger.error('Can\'t connect to source {} for user {}!'.format(
                user_source.source.label, user_source.user.username))


def save_to_db(articles, user_source):
    """Save parsed articles to database"""

    for article in articles:
        if article.get('header'):
            article = Article(
                source=user_source.source,
                url=article.get('url'),
                header=article.get('header'),
                text=article.get('text')
            )
            article.save()
            article.users.add(user_source.user)

            logger.info('Created new article {} with url: {}'.format(article.id, article.url))
        elif article.get('db_article'):
            article = article.get('db_article')
            if user_source.user not in article.users.all():
                article.users.add(user_source.user)
                logger.info('Updated new article with id: {} for user: {}'.format(article.id, user_source.user.id))
