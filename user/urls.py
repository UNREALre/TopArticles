from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreate, UserUpdate


app_name = 'user'

urlpatterns = [
    path('get-token/', obtain_auth_token, name='get_token'),
    path('create/', UserCreate.as_view(), name='create_user'),
    path('update/', UserUpdate.as_view(), name='update_user')
]
