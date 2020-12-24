from django import forms
from django.forms import inlineformset_factory

from main.models import Post, AdditionalImage


class SearchForm(forms.Form):
    pass


class PostForm(forms.Form):
    pass


class CommentForm(forms.Form):
    pass


AIFormSet = inlineformset_factory(Post, AdditionalImage, fields='__all__')
