from abc import ABC

from rest_framework import serializers

from main.models import Rubric, Post




class VideoSerializer(serializers.ModelSerializer):
    """Для сравнения данных с сайтом"""

    class Meta:
        model = Post
        fields = ('link', 'title', 'content', 'published')
