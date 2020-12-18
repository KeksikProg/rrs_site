from django.test import TestCase
import collections

from main.models import Rubric, Post
from main.serializers import VideoSerializer
from main.util import get_data


class SerializerTestCase(TestCase):
    def test_serializer_and_xml_data(self):
        rubric1 = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(
            rubric=rubric1,
            link='https://www.youtube.com/watch?v=Cpc3yeW0eJE',
            title='Играю в пубг',
            content=None,
            published='2019-09-15T18:21:25+00:00',
            image='',
            author='maxek',
            is_active=True)
        post2 = Post.objects.create(
            rubric=rubric1,
            link='https://www.youtube.com/watch?v=3WCT5rBh318',
            title='Обновление в бравл Старс',
            content=None,
            published='2019-09-15T16:27:20+00:00',
            image='',
            author='maxek',
            is_active=True)
        ser_data = VideoSerializer([post1, post2], many=True).data
        xml_data = get_data(url='https://www.youtube.com/feeds/videos.xml?channel_id=UCNNnJK87LJ6pAd77iRZEcpg')
        self.assertEqual(ser_data, xml_data)
