from django.core.management.base import BaseCommand, CommandError
from top_parser.do_parse import start_process


class Command(BaseCommand):
    help = 'Starts parsing process'

    def handle(self, *args, **options):
        start_process()
