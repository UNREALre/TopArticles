from django.shortcuts import render
from django.http import HttpResponse

from .do_parse import start_process


def do_parse(request):
    start_process()
    return HttpResponse('test')
