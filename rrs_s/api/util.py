from django_filters import rest_framework as filters
from main.models import Post, Comments


# filters
class CharFilterInFilter(filters.CharFilter, filters.BaseInFilter):
    """Класс фильтрации ,который просто объединяет в себе 2 других класса фильтрации
    1. для того, чтобы можно было искать по словам CharFilter
    2. Для того, чтобы можно было использовать in для фильтрации BaseInFilter"""

    pass


class PostFilter(filters.FilterSet):
    """Фильтр для постов, будет производить фильтрацию по рубрикам"""

    rubric = CharFilterInFilter(field_name='rubric__slug', lookup_expr='in')

    class Meta:
        model = Post
        fields = ['rubric']


class CommentsFilter(filters.FilterSet):
    """Фильтр коммментариев, который будет производить фильтрацию по постам(а то это бесполезно)"""

    post = CharFilterInFilter(field_name='post__slug', lookup_expr='in')

    class Meta:
        model = Comments
        fields = ['post']
