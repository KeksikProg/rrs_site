import main
from main.models import Post, Rubric
from main.util import get_data_from_xml
from rrs_s.celery import app

"""В этом файле у нас будут храниться таски"""


@app.task
def check_videos_and_create():
    """Таска которая будет брать инфу из xml отображения канала ютуб и создавать объекты видео"""

    data = get_data_from_xml()
    for item in data:
        try:
            Post.objects.get(link=item['link'])  # title=item['title'], published=item['published']
        except main.models.Post.DoesNotExist:
            Post.objects.create(
                rubric=Rubric.objects.get(title='Видео'),
                link=item['link'],
                title=item['title'],
                content=item['content'],
                published=item['published'],
                image='',
                author='maxek',
                is_active=True)
