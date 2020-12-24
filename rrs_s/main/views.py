from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from main.forms import SearchForm, PostForm, AIFormSet, CommentForm
from main.models import Rubric, Post, Comments


# other
def home(request):
    """Домашня страница, она будет главной"""

    posts = Post.objects.all()[:10]
    context = {'posts': posts}

    return render(request, 'main/home.html', context)


def docs(request, docs_page):
    """Будет делать из страниц с документами в формате хтмл страницы сайта и запрашивать их по странице"""

    try:
        template = get_template(f'main/{docs_page}.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


# posts
def by_rubric(request, slug):
    """Вывод записей по какой-то определенной рубрике (есть поиск и пагинация страниц)"""

    rubric = get_object_or_404(Rubric, slug=slug)
    posts = Post.objects.filter(rubric=rubric)

    """Search"""
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        posts.filter(q)
    else:
        keyword = ''
    form = SearchForm(inital={'keyword': keyword})

    """paginator"""
    paginator = Paginator(posts, 5)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'posts': page.objects.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)


def add_posts(request):
    """Функция, которая будет добавлять объекты записей, статьи"""

    if request.method == 'POST':
        rubric_article = get_object_or_404(Rubric, pk=2)
        forms = PostForm(request.POST, request.FILES)
        if forms.is_valid():
            post = forms.save()
            post.rubric = rubric_article
            formset = AIFormSet(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, message='Пост будет добавлен после проверки модератором! Спасибо!')
                return redirect('main:home')
    else:
        forms = PostForm(initial={})
        formset = AIFormSet()
    context = {'forms': forms, 'formset': formset}
    return render(request, 'main/add_posts.html', context)


@staff_member_required
def change_posts(request, slug):
    """change posts (only staff)"""

    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, message='Статья была изменена!')
                return redirect('main:post_detail', {'slug': slug})
    else:
        form = PostForm(instance=post)
        formset = AIFormSet(instance=post)
    context = {'form': form, 'formset': formset}
    return render(request, 'main/change_posts.html', context)


@staff_member_required
def delete_posts(request, slug):
    """Delete posts (only staff)"""

    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.add_message(request, messages.SUCCESS, message='Статья удалена!')
        return redirect('main:home')
    else:
        context = {'post': post}
        return render(request, 'main/delete_posts.html', context)


@login_required(login_url='/user/login/')
def posts_detail(request, slug):
    """Детальное отображение поста (только авторизованные пользователи)"""

    post = get_object_or_404(Post, slug=slug)
    ai = post.additionalimage_set.all()  # Тут мы берем дополнительные изображения через такую функцию
    comments = Comments.objects.filter(post=post)
    initial = {'post': post.pk, 'author': request.user.username}
    form = CommentForm(initial=initial)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            response = c_form.save()
            response.author = request.user.username
            response.save()
            messages.add_message(request, messages.SUCCESS, message='Комментарий успешно добавлен')
            return redirect('main:post_detail', {'slug': slug})
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, message='Комментарий не был добавлен!')
    context = {'post': post, 'ai': ai, 'comments': comments, 'form': form}
    return render(request, 'main/detail.html', context)
