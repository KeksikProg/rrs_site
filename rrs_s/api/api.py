from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.serializers import RubricListAndCreateSerializer, PostListSerializer, PostDetailSerializer, CommentsListAndCreateSerializer, PostCreateSerializer
from api.util import PostFilter, CommentsFilter
from main.models import Rubric, Post, Comments

SAFE_ACTIONS = ['list', 'retrieve'] # Безопасные действия, которые не меняют базу данных


class RubricViewSet(viewsets.ModelViewSet):
    """Сет для вывода и создания рубрик"""

    serializer_class = RubricListAndCreateSerializer

    def list(self, request, **kwargs):
        """Не пользуемся стандартной функцией лист потому что из-за неё происходит ошибка 'RenameAttributes'"""

        queryset = Rubric.objects.all()
        serializer_data = RubricListAndCreateSerializer(queryset, many=True).data
        return Response(serializer_data)

    def get_permissions(self):
        """Для какие действия, какие нужны права"""

        if self.action in SAFE_ACTIONS:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    """Для вывода деталей поста, списка постов и для создания постов"""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter  # Наш фильтр благодаря которому мы можем фильтровать посты по рубрикам через параметры урл
    lookup_field = 'slug'  # Поле на которое смотреть при фильтрации
    permission_classes = [IsAuthenticated]  # Права
    queryset = Post.objects.filter(is_active=True)  # Будем выводить только активные посты, как не страно

    def get_serializer_class(self):
        """Переназначаем метод, тк нам нужно, чтобы в разные моменты были разные сериализаторы"""

        if self.action == 'list':
            return PostListSerializer  # Для списка постов
        elif self.action == 'retrieve':
            return PostDetailSerializer  # Для детального вывода постов
        elif self.action == 'create':
            return PostCreateSerializer  # Для создания постов

    def perform_create(self, serializer):
        if self.request.user.is_staff:  # Если пользователь работник сайта, то нам не нужно, чтобы его пост проходил проверку
            serializer.save(is_active=True)
        else:  # Если пост делает обычный человек, то мы просто сохраняем без актива
            serializer.save()


class CommentsViewSet(viewsets.ModelViewSet):
    """Для вывода списка комментариев и для их создания"""

    serializer_class = CommentsListAndCreateSerializer  # У нас один сериализатор для создания и для вывода списка, там поля не меняются
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentsFilter  # Фильтрация по постам, если будет просто список комментариев это будет бессмысленно
    lookup_field = 'slug'
    queryset = Comments.objects.all()
    permission_classes = [IsAuthenticated] #Права
