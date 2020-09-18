from django.urls import path

from .views import UserCreate


app_name = 'user'

urlpatterns = [
    path('create/', UserCreate.as_view())
]
