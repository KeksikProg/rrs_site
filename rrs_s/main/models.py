from django.contrib.auth.models import AbstractUser
from django.db import models
from uuslug import slugify

from main.util import get_timestamp_path


class Client(AbstractUser):
    """Модель пользователя"""

    is_active = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Прошел активацию?',
    )
    slug = models.SlugField(
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    """Рубрики"""
    title = models.CharField(
        max_length=255,
        verbose_name='Название'

    )
    slug = models.SlugField(
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['title']


class Post(models.Model):
    """Посты или видео"""
    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
        default=2
    )
    link = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Ссылка(для видео)',
        unique=True
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
        unique=True,
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='Фотография'
    )
    author = models.CharField(
        max_length=150,
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Добавлено',
        null=True
    )
    published = models.DateTimeField(
        db_index=True,
        null=True,
        verbose_name='Опубликовано(для видео)'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активация'
    )
    slug = models.SlugField(
        unique=True
    )

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    """Дополнительные фотографии, будут вместе с постами или видео"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'

    )
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='Дополнительная фотография'
    )

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Дополнительная фотография'
        verbose_name_plural = 'Дополнительные фотографии'


class Comments(models.Model):
    """Комментарии"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    author = models.CharField(
        max_length=150,
        verbose_name='Автор'
    )
    content = models.TextField(
        max_length=400,
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Написан'
    )

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
