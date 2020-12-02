from django_filters import rest_framework as filters
from main.models import Post, Comments


class CharFilterInFilter(filters.CharFilter, filters.BaseInFilter):
    pass


class PostFilter(filters.FilterSet):
    rubric = CharFilterInFilter(field_name='rubric__slug', lookup_expr='in')

    class Meta:
        model = Post
        fields = ['rubric']


class CommentsFilter(filters.FilterSet):
    post = CharFilterInFilter(field_name='post__slug', lookup_expr='in')

    class Meta:
        model = Comments
        fields = ['post']
