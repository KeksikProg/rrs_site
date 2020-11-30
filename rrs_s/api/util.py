from django_filters import rest_framework as filters
from main.models import Post


class CharFilterInFilter(filters.CharFilter, filters.BaseInFilter):
    pass


class PostFilter(filters.FilterSet):
    rubric = CharFilterInFilter(field_name='rubric__slug', lookup_expr='in')

    class Meta:
        model = Post
        fields = ['rubric']
