from rest_framework import serializers

from main.models import Rubric, Post, Comments


class PostListSerializer(serializers.ModelSerializer):
    """Сериализатор списка постов"""

    class Meta:
        model = Post
        fields = ('rubric', 'title', 'image', 'author', 'created_at', 'slug')


class PostCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания постов"""

    class Meta:
        model = Post
        fields = ('rubric', 'title', 'content', 'image', 'author',)


class PostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор детального отображения постов"""

    class Meta:
        model = Post
        fields = ('rubric', 'title', 'content', 'image', 'author', 'created_at',)


class RubricListAndCreateSerializer(serializers.ModelSerializer):
    """Сериализатор списка и создания рубрик"""

    class Meta:
        model = Rubric
        fields = ('title',)


class CommentsListAndCreateSerializer(serializers.ModelSerializer):
    """Сериализатор списка и создания комментариев"""

    class Meta:
        model = Comments
        fields = ('post', 'author', 'content', 'created_at')

