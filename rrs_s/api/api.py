from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from api.serializers import RubricListSerializer, PostListSerializer, PostDetailSerializer
from api.util import PostFilter
from main.models import Rubric, Post
from rest_framework.generics import ListAPIView


class RubricViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Rubric.objects.all()
        serializer_data = RubricListSerializer(queryset, many=True).data
        return Response(serializer_data)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Переназначаем метод, тк нам нужно, чтобы в разные моменты были разные сериализаторы"""

        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(is_active = True)
        return queryset
