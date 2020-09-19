from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from .models import Source
from .serializers import SourceSerializer


class SourceView(ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SourceCreateView(CreateAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = (IsAdminUser, )


class SingleSourceView(RetrieveUpdateDestroyAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = (IsAdminUser, )
