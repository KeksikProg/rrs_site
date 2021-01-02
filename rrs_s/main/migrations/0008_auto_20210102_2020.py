# Generated by Django 3.1.3 on 2021-01-02 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210102_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='donations',
        ),
        migrations.AlterField(
            model_name='additionalimage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.post', verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.post', verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активация'),
        ),
        migrations.DeleteModel(
            name='Donations',
        ),
    ]
