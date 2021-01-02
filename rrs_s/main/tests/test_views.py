from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from loguru import logger

from main.models import Rubric, Post, Comments
from main.views import home, docs, by_rubric, add_posts


class ViewsTestCase(TestCase):
    """testing function views"""

    def test_home(self):
        url = reverse('main:home')
        response_content = self.client.get(url).content.decode('utf-8')
        exp_content = render_to_string('main/home.html')

        self.assertEqual(exp_content, response_content)

    def test_docs(self):
        url = reverse('main:docs', kwargs={'docs_page': 1})
        response_content = self.client.get(url).content.decode('utf-8')
        exp_content = render_to_string('main/1.html')

        self.assertEqual(exp_content, response_content)

    def test_error_docs(self):
        url = reverse('main:docs', kwargs={'docs_page': -1})
        response_status = self.client.get(url).status_code

        self.assertEqual(404, response_status)

    def test_by_rubric(self):
        rubric = Rubric.objects.create(title='Видео')
        url = reverse('main:by_rubric', kwargs={'slug': 'video'})
        response_content = self.client.get(url).content.decode('utf-8')
        exp_data = render_to_string('main/by_rubric.html')

        self.assertEqual(exp_data, response_content)

    def test_add_posts(self):
        Rubric.objects.create(pk=2, title='Статьи')
        url = reverse('main:add_posts')
        response = self.client.get(url)
        data = {'title': 'keks', 'content': 'real keksik', 'image': '', 'csrfmiddlewaretoken': response.context['csrf_token']}
        management_form = response.context['formset'].management_form

        for i in 'TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS':
            data['%s-%s' % (management_form.prefix, i)] = management_form[i].value()

        for i in range(response.context['formset'].total_form_count()):
            current_form = response.context['formset'].forms[i]

            for field_name in current_form.fields:
                if current_form[field_name] == 'DELETE':
                    pass
                value = current_form[field_name].value()
                data['%s-%s' % (current_form.prefix, field_name)] = value if value is not None else ''
            else:
                continue

        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)

    def test_change_post(self):
        rubric = Rubric.objects.create(title='Статьи')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        url = reverse('main:change_posts', kwargs={'slug': post1.slug})
        response = self.client.get(url)
        data = {'title': 'keks_test', 'content': 'content_test', 'image': '', 'csrfmiddlewaretoken': response.context['csrf_token']}
        management_form = response.context['formset'].management_form

        for i in 'TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS':
            data['%s-%s' % (management_form.prefix, i)] = management_form[i].value()

        for i in range(response.context['formset'].total_form_count()):
            current_form = response.context['formset'].forms[i]

            for field_name in current_form.fields:
                if current_form[field_name] == 'DELETE':
                    pass
                value = current_form[field_name].value()
                data['%s-%s' % (current_form.prefix, field_name)] = value if value is not None else ''
            else:
                continue

        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)

    def test_delete_posts(self):
        """Need off decorator @staff_member_required"""

        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        url = reverse('main:delete_posts', kwargs={'slug': post1.slug})
        response_code = self.client.post(url).status_code
        self.assertEqual(302, response_code)

    def test_detail_post(self):
        """Need off login_required"""

        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        url = reverse('main:detail_post', kwargs={'slug': post1.slug})
        response_content = self.client.get(url).content.decode('utf-8')
        exp_data = render_to_string('main/detail.html')
        self.assertEqual(exp_data, response_content)

    def test_detail_post_comments(self):
        rubric = Rubric.objects.create(title='Видео')
        post1 = Post.objects.create(rubric=rubric,
                                    title='keks',
                                    content='real keks',
                                    image='',
                                    author='maxek',
                                    is_active=True)
        data = {'content': 'Нехуительный пост'}
        url = reverse('main:detail_post', kwargs={'slug': post1.slug})
        response_code = self.client.post(url, data).status_code
        self.assertEqual(302, response_code)
