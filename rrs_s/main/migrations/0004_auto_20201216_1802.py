# Generated by Django 3.1.3 on 2020-12-16 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201214_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
