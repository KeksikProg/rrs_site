from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import RubricListAndCreateSerializer, PostListSerializer, PostDetailSerializer, CommentsListAndCreateSerializer
from main.models import Rubric, Post, Comments

"""Для тестирования ViewSet-ов и в целом API
Перед проверкой надо оключать permissions, к сожалению хз как это щас поправить"""

c = Client()  # Для того, чтобы имитировать клиента


class ApiTestCase(APITestCase):
    """Один тест кейс для всего"""

    # testing get requests
    def test_get_list_rubric(self):
        rubric1 = Rubric.objects.create(title='Видео')
        rubric2 = Rubric.objects.create(title='Статьи')
        url = reverse('api:rubrics-list')
        response = c.get(url)
        serializer_data = RubricListAndCreateSerializer([rubric1, rubric2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_posts(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        post2 = Post.objects.create(rubric=rubric,
                                    title='keksik',
                                    content='real keksik',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        url = reverse('api:posts-list')
        response = c.get(url)
        serializer_data = PostListSerializer([post2, post1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_list_comments(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        comment = Comments.objects.create(post=post1, author='maxek', content='real keks')
        url = reverse('api:comments-list')
        response = c.get(url)
        serializer_data = CommentsListAndCreateSerializer([comment, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_detail_posts(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        url = reverse('api:posts-detail', kwargs={'slug': post1.slug})
        response = c.get(url)
        serializer_data = PostDetailSerializer(post1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # testing post requests
    def test_post_rubrics(self):
        url = reverse('api:rubrics-create')
        response = c.post(url, data={'title': 'Статьи'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_comments(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        url = reverse('api:comments-create')
        response = c.post(url, data={'post': f'{post1.you_id}', 'author': 'maxek', 'content': 'real keks'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post_posts(self):
        rubric = Rubric.objects.create(title='Видео')

        url = reverse('api:posts-create')
        response = c.post(url, data={'rubric': f'{rubric.you_id}', 'title': 'keks', 'content': 'real keks', 'image': '', 'author': 'maxek', })
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
