from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    def test_home(self):
        url = '/'
        print(url)
        result = self.client.get(url).content
        r_result = b'Hello World'
        self.assertEqual(r_result, result)