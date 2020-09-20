from django.urls import path

from . import views

app_name = 'top_parser'

urlpatterns = [
    path('', views.do_parse, name='parser'),
]
