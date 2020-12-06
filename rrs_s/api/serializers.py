from rest_framework import serializers

from main.models import Rubric, Post, Comments


class PostListSerializer(serializers.ModelSerializer):
    """Сериализатор списка постов"""

    class Meta:
        # list_serializer_class = FilterPostSerializer Из-за этого модуля не работает django_filters который нужнее
        model = Post
        fields = ('rubric', 'title', 'image', 'author', 'created_at', 'slug')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('rubric', 'title', 'content', 'image', 'author',)


class PostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор детального отображения постов"""

    class Meta:
        model = Post
        fields = ('rubric', 'title', 'content', 'image', 'author', 'created_at',)


class RubricListAndCreateSerializer(serializers.ModelSerializer):
    """Сериализатор рубрик"""

    class Meta:
        model = Rubric
        fields = ('title',)


class CommentsListAndCreateSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    class Meta:
        model = Comments
        fields = ('post', 'author', 'content', 'created_at')

# class FilterPostSerializer(serializers.ListSerializer):
#     """Этот фильтр конфликтует с другим фильтром, пока не решу включать не буду"""
#
#     def to_representation(self, data):
#         data = data.filter(is_active=True)
#         return super().to_representation(data)
