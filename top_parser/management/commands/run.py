# -*- coding: utf-8 -*-
"""
This module contains class-command 'run'. Used to fire parsing process within CRON tasks or manual calls.

Example of call: python manage.py run
"""

from django.core.management.base import BaseCommand, CommandError
from top_parser.do_parse import start_process


class Command(BaseCommand):
    help = 'Starts parsing process'

    def handle(self, *args, **options):
        start_process()
