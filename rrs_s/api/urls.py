from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.api import RubricViewSet, PostViewSet, CommentsViewSet

urlpatterns = (
    path('rubrics/', RubricViewSet.as_view({'get': 'list'}), name='rubrics'),
    path('posts/list/', PostViewSet.as_view({'get': 'list'}), name='posts-list'),
    path('posts/<slug:slug>/', PostViewSet.as_view({'get': 'retrieve'}), name='posts-detail'),
    path('posts/comments-list', CommentsViewSet.as_view({'get': 'list'}), name='comments-list'),
)
