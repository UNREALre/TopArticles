from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SourceView, SourceCreateView, SingleSourceView, ArticleViewSet


app_name = 'article'

router = DefaultRouter()
router.register(r'', ArticleViewSet, basename='articles')

urlpatterns = [
    path('sources/', SourceView.as_view(), name='sources_list'),
    path('sources/create/', SourceCreateView.as_view(), name='source_create'),
    path('sources/<int:pk>/', SingleSourceView.as_view(), name='source_view_update_delete')
] + router.urls
