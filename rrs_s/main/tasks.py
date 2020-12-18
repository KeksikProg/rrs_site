import main
from main.models import Post, Rubric
from main.util import get_data


def check_videos_and_create(data=get_data()):
    for item in data:
        try:
            Post.objects.get(title=item['title'])
        except main.models.Post.DoesNotExist:
            post1 = Post.objects.create(
                rubric=Rubric.objects.get(title='Видео'),
                link=item['link'],
                title=item['title'],
                content=item['content'],
                published=item['published'],
                image='',
                author='maxek',
                is_active=True)
            print(post1)
