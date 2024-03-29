from main.models import Rubric


def rubric_context_processor(request):
    """Будет добавлять в контекст каждого шаблона рубрики, поисковые слова и страницы"""

    context = {'rubric': Rubric.objects.all(), 'keyword': '', 'all': ''}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
