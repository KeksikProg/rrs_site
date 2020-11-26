from rest_framework import serializers

from main.models import Rubric, Post, Comments


class RubricListSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Rubric
        fields = ('title',)


class FilterPostSerializer(serializers.ListSerializer):
    """"""

    @staticmethod
    def to_representation(data):
        data = data.filter(is_active=True)
        return super().to_representation(data)


class PostListSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        list_serializer_class = FilterPostSerializer
        model = Post
        fields = ('rubric', 'title', 'content', 'image', 'author', 'created_at',)


class CommentListSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Comments
        fields = ('__all__',)


class PostDetailSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Post
        fields = ('rubric', 'title', 'content', 'image', 'author', 'created_at',)
