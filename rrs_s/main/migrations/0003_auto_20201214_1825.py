# Generated by Django 3.1.3 on 2020-12-14 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201124_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.CharField(max_length=255, null=True, verbose_name='Ссылка(для видео)'),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='Опубликовано(для видео)'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
