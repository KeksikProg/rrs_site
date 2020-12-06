from django.urls import path
from api.api import RubricViewSet, PostViewSet, CommentsViewSet

urlpatterns = (
    # rubrics
    path('rubrics_list/', RubricViewSet.as_view({'get': 'list'}), name='rubrics-list'),
    path('rubrics_create/', RubricViewSet.as_view({'post': 'create'}), name='rubrics-create'),

    # posts
    path('posts_list/', PostViewSet.as_view({'get': 'list'}), name='posts-list'),
    path('posts_detail/<slug:slug>/', PostViewSet.as_view({'get': 'retrieve'}), name='posts-detail'),
    path('posts_create/', PostViewSet.as_view({'post': 'create'}), name='posts-create'),

    # comments
    path('posts_comments_list/', CommentsViewSet.as_view({'get': 'list'}), name='comments-list'),
    path('posts_comments_create/', CommentsViewSet.as_view({'post': 'create'}), name='comments-create')
)
