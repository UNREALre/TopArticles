from rest_framework.generics import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class UserUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
