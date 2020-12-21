from django.test import TestCase

from api.serializers import RubricListAndCreateSerializer, PostListSerializer, CommentsListAndCreateSerializer, PostDetailSerializer, PostCreateSerializer
from main.models import Rubric, Post, Comments

"""Тесты для проверки сериализаторов"""
"""Для их проверки не надо отключать Permissions, они тут ничего не значат"""


class SerializersTestCase(TestCase):
    """Опять один тест кейс для всего"""

    def test_rubric(self):
        rubric1 = Rubric.objects.create(title='Видео')
        rubric2 = Rubric.objects.create(title='Кекс')
        data = RubricListAndCreateSerializer([rubric1, rubric2], many=True).data
        exp_data = [
            {'title': rubric1.title},
            {'title': rubric2.title}
        ]
        self.assertEqual(exp_data, data)

    def test_post_detail(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        data = PostDetailSerializer(post1).data
        exp_data = {
            'rubric': rubric.you_id,
            'title': 'keks',
            'content': 'real keks',
            'image': None,
            'author': 'maxek',
            'created_at': data['created_at']
        }
        self.assertEqual(exp_data, data)

    def test_list_post(self):
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
        data = PostListSerializer([post1, post2], many=True).data
        exp_data = [
            {
                'rubric': rubric.you_id,
                'title': 'keks',
                'image': None,
                'author': 'maxek',
                'created_at': data[0]['created_at'],
                'slug': 'keks'
            },
            {
                'rubric': rubric.you_id,
                'title': 'keksik',
                'image': None,
                'author': 'maxek',
                'created_at': data[1]['created_at'],
                'slug': 'keksik'
            }
        ]
        self.assertEqual(exp_data, data)

    def test_comments(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        comment = Comments.objects.create(post=post1, author='maxek', content='keks')
        data = CommentsListAndCreateSerializer(comment).data
        exp_data = {
            'post': post1.you_id,
            'author': 'maxek',
            'content': 'keks',
            'created_at': data['created_at']
        }
        self.assertEqual(exp_data, data)

    def test_create_post(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        data = PostCreateSerializer(post1).data
        exp_data = {'rubric': rubric.you_id,
                    'title': 'keks',
                    'content': 'real keks',
                    'image': None,
                    'author': 'maxek', }
        self.assertEqual(exp_data, data)
