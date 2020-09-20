"""
Main parsing process goes here.
"""

import logging
import top_parser.parsers as top_parser
from top_news.helpers import AESCipher

from user.models import UserSource


def start_process():
    user_sources = UserSource.objects.all()
    for user_source in user_sources:
        auth_data = {
            'login': user_source.login,
            'password': AESCipher(user_source.password, user_source.user.password).decrypt()
        }

        parser = top_parser.factory.create(user_source.label, **auth_data)
        if parser and parser.test_connection():
            logging.info('Successfully connected to source {} for user {}'.format(
                user_source.label, user_source.user.username))
        else:
            print("FAIL")
            logging.error('Can\'t connect to source {} for user {}!'.format(
                user_source.label, user_source.user.username))
