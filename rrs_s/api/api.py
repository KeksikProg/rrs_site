from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from api.serializers import RubricListAndCreateSerializer, PostListSerializer, PostDetailSerializer, CommentsListAndCreateSerializer, PostCreateSerializer
from api.util import PostFilter, CommentsFilter
from main.models import Rubric, Post, Comments
from rest_framework.generics import ListAPIView, CreateAPIView

SAFE_ACTIONS = ['list', 'retrieve']


class RubricViewSet(viewsets.ModelViewSet):
    """Сет для вывода и создания рубрик"""
    serializer_class = RubricListAndCreateSerializer

    def list(self, request, **kwargs):
        queryset = Rubric.objects.all()
        serializer_data = RubricListAndCreateSerializer(queryset, many=True).data
        return Response(serializer_data)

    # def get_permissions(self):
    #     if self.action in SAFE_ACTIONS:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    """Для детального вывода и списка постов"""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
    lookup_field = 'slug'  # Поле на которое смотреть при фильтрации
    # permission_classes = [IsAuthenticated]  # Права
    queryset = Post.objects.filter(is_active=True)

    def get_serializer_class(self):
        """Переназначаем метод, тк нам нужно, чтобы в разные моменты были разные сериализаторы"""

        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action == 'create':
            return PostCreateSerializer

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save(is_active=True)
        else:
            serializer.save()


class CommentsViewSet(viewsets.ModelViewSet):
    """"""

    serializer_class = CommentsListAndCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentsFilter
    lookup_field = 'slug'
    queryset = Comments.objects.all()
    # permission_classes = [IsAuthenticated]
