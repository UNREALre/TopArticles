from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     RetrieveUpdateDestroyAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, permissions

from .models import Source, Article
from .serializers import (SourceSerializer, ArticleSerializer,
                          ArticleDetailSerializer, ArticleListSerializer)


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


class ArticlePermission(permissions.BasePermission):
    """Permissions for different API actions"""

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return request.user.is_authenticated
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        else:
            return False


class ArticleViewSet(viewsets.ModelViewSet):
    """Main View Set for all CRUD operations with Articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (ArticlePermission, )

    def list(self, request, *args, **kwargs):
        self.serializer_class = ArticleListSerializer
        return super(ArticleViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ArticleDetailSerializer
        return super(ArticleViewSet, self).retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        source = get_object_or_404(Source, id=self.request.data.get('source_id'))
        return serializer.save(source=source)

    def perform_update(self, serializer):
        source = get_object_or_404(Source, id=self.request.data.get('source_id'))
        return serializer.save(source=source)
