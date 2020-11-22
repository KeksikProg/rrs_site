from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from main.util import get_timestamp_path, is_active_post


class Donations(models.Model):
    """Донаты пользователя или является ли он спонсором"""
    sponsor = models.BooleanField(
        default=False,
        verbose_name='Является спонсором?'
    )
    donats = models.DecimalField(
        max_digits=100,
        decimal_places=2,
        default=0,
        verbose_name='Донаты'
    )


class Client(AbstractUser):
    """Модель пользователя"""

    is_active = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Прошел активацию?',
    )
    donations = models.ForeignKey(
        Donations,
        on_delete=models.CASCADE
    )

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    """Рубрики"""
    title = models.CharField(
        max_length=255,
        verbose_name='Название'

    )

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
        verbose_name='Рубрика'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    content = models.TextField(
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
        verbose_name='Добавлено'
    )
    is_active = models.BooleanField(
        default=is_active_post
    )

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,

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
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
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
