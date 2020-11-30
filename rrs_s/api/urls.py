from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.api import RubricViewSet, PostViewSet

urlpatterns = (
    path('rubrics/', RubricViewSet.as_view({'get': 'list'})),
    path('posts/list/', PostViewSet.as_view({'get': 'list'})),
    path('posts/<slug:slug>/', PostViewSet.as_view({'get': 'retrieve'})),
)
