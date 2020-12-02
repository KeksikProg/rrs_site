from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import RubricListSerializer, PostListSerializer, PostDetailSerializer, CommentListSerializer
from main.models import Rubric, Post, Comments


class ApiTestCase(APITestCase):
    def test_get_list_rubric(self):
        rubric1 = Rubric.objects.create(title='Видео')
        rubric2 = Rubric.objects.create(title='Статьи')
        url = reverse('api:rubrics')
        response = self.client.get(url)
        serializer_data = RubricListSerializer([rubric1, rubric2], many=True).data
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
        response = self.client.get(url)
        serializer_data = PostListSerializer([post2, post1], many=True).data
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
        response = self.client.get(url)
        serializer_data = PostDetailSerializer(post1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

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
        response = self.client.get(url)
        serializer_data = CommentListSerializer([comment, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])
