from django.urls import path

from .views import SourceView, SourceCreateView, SingleSourceView


app_name = 'article'

urlpatterns = [
    path('sources/', SourceView.as_view(), name='sources_list'),
    path('sources/create/', SourceCreateView.as_view(), name='source_create'),
    path('sources/<int:pk>/', SingleSourceView.as_view(), name='source_view_update_delete')
]
