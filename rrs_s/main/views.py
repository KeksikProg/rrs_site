from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.core.signing import BadSignature
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import django.template
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from main.forms import SearchForm, PostForm, AIFormSet, CommentForm, ClientRegForm, ChangeUserInfoForm
from main.models import Rubric, Post, Comments, Client

# other
from main.util import signer


def home(request):
    """Домашня страница, она будет главной"""

    posts = Post.objects.all()[:10]
    context = {'posts': posts}

    return render(request, 'main/home.html', context)


def docs(request, docs_page):
    """Будет делать из страниц с документами в формате хтмл страницы сайта и запрашивать их по странице"""

    try:
        template = get_template(f'main/{docs_page}.html')
    except django.template.TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        raise Http404
    user = get_object_or_404(Client, username=username)
    if user.is_active:
        messages.add_message(request, messages.INFO, message='Пользователь уже был активирован')
        reverse_lazy('main:home')
    else:
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, message='Пользователь активирован!')
        reverse_lazy('main:home')


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
    form = SearchForm(initial={'keyword': keyword})

    """paginator"""
    paginator = Paginator(posts, 5)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'posts': page.object_list, 'form': form}
    return render(request, 'main/by_rubric.html', context)


def add_posts(request):
    """Функция, которая будет добавлять объекты записей, статьи"""

    if request.method == 'POST':
        forms = PostForm(request.POST, request.FILES)
        if forms.is_valid():
            article = forms.save()
            formset = AIFormSet(request.POST, request.FILES, instance=article)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, message='Статья успешно написана!')
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
                return redirect('main:detail_post', slug)
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
def detail_post(request, slug):
    """Детальное отображение поста (только авторизованные пользователи)"""

    post = get_object_or_404(Post, slug=slug)
    ai = post.additionalimage_set.all()  # Тут мы берем дополнительные изображения через такую функцию
    comments = Comments.objects.filter(post=post)
    form = CommentForm()
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            response = c_form.save(commit=False)
            response.author = request.user.username
            response.post = post
            response.save()
            messages.add_message(request, messages.SUCCESS, message='Комментарий успешно добавлен')
            return redirect('main:detail_post', slug)
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, message='Комментарий не был добавлен!')
    context = {'post': post, 'ai': ai, 'comments': comments, 'form': form}
    return render(request, 'main/detail.html', context)


# Authorization
class CLogin(LoginView):
    """Login View (Django classic)"""

    template_name = 'main/login.html'


class CLogout(LogoutView):
    """Logout View (Django classic)"""

    template_name = 'main/logout.html'


# User
class ClientRegView(CreateView):
    """Для регистрации пользователей"""

    model = Client
    template_name = 'main/register.html'
    form_class = ClientRegForm
    success_url = reverse_lazy('main:login')


class ClientRegisterDone(TemplateView):
    """Просто выводит шаблон о том, что пользователь создан и его надо всего лишь подтвердить"""
    template_name = 'main/client_register_done.html'


class ChangeUserInfo(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    model = Client
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Личные данные былы успешно изменены!'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return super().get_object(queryset, pk=self.user_id)


class ChangeClientPassword(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'main/change_client_password.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль успешно изменен!'


class DeleteClientView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    template_name = 'main/delete_client.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Пользователь успешно удален!'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, message='Пользователь успешно удален!')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# Reset password
class ClientResetView(PasswordResetView):
    template_name = 'main/password_reset_form.html'
    subject_template_name = 'email/password_reset_subj.txt'
    email_template_name = 'email/password_reset_body.html'
    success_url = reverse_lazy('main:password_reset_done')


class ClientPasswordResetDone(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class ClientPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm_view.html'
    success_url = reverse_lazy('main:login')
