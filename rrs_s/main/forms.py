from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from main.models import Post, AdditionalImage, Comments, Client


class SearchForm(forms.Form):
    """Поисковая форма не привязанная к модели"""

    keyword = forms.CharField(
        required=False,
        max_length=255,
        label=''
    )


class PostForm(forms.ModelForm):
    """Форма для постов, тк через данную view будут делаться только статьи, то рубрику и автора добавляем сами, а не просим пользователя"""

    class Meta:
        model = Post
        fields = ('rubric', 'title', 'content', 'author', 'image')
        widgets = {'created_at': forms.HiddenInput, 'author': forms.HiddenInput, 'rubric': forms.HiddenInput}


class CommentForm(forms.ModelForm):
    """Форма для комментариев, автор и пост будут сами добавлятся"""

    class Meta:
        model = Comments
        fields = '__all__'
        widgets = {'post': forms.HiddenInput, 'author': forms.HiddenInput}


class ClientRegForm(forms.ModelForm):
    """Форма для регистрации пользователей"""

    email = forms.EmailField(
        required=True,
        label='Электронная почта'
    )
    pass1 = forms.CharField(
        label='',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    pass2 = forms.CharField(
        label='',
        widget=forms.PasswordInput,
    )

    def clean(self):
        """Проверяем одиннаковые ли пароли ввел пользователь"""

        passw1 = self.cleaned_data['pass1']
        if passw1:
            password_validation.validate_password(passw1)
        super().clean()
        passw2 = self.cleaned_data['pass2']
        if passw1 and passw2 and passw1 != passw2:
            errors = {
                'pass2': ValidationError('Пароли не совпадают, попробуйте ещё раз', code='password_missmatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        """Сохраняем пользователя"""

        client = super().save(commit=False)
        client.set_password(self.cleaned_data['pass1'])
        if commit:
            client.save()
        return client

    class Meta:
        model = Client
        fields = ('username', 'email', 'pass1', 'pass2', 'first_name', 'last_name')


class ChangeUserInfoForm(forms.Form):
    """Форма с помощью которой пользователь сможет сменить личные данные"""

    class Meta:
        model = Client
        fields = ('username', 'email', 'first_name', 'last_name')


AIFormSet = inlineformset_factory(Post, AdditionalImage, fields='__all__')
