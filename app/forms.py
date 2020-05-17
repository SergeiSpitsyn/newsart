"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class PollForm(forms.Form):
    """Poll form on 'pool.html' page."""
    name = forms.CharField(label='Ваше имя:', max_length=100)
    gender = forms.ChoiceField(label='Ваш пол:',
                               choices=[('1', 'мужской'), ('2', 'женский'),],
                               widget=forms.RadioSelect, initial=1)
    age = forms.IntegerField(label='Ваш возраст:', min_value=1, max_value=128)
    conven = forms.ChoiceField(label='Оцените удобство расположения элементов сайта',
                             choices=(('5', 'Идеальное'),
                                      ('4', 'Интуитивно понятное'),
                                      ('3', 'Могло быть лучше'),
                                      ('2', 'Сильно запутанное'),
                                      ('1', 'Плохое')), initial=5)
    mark = forms.ChoiceField(label='Как бы Вы оценили сайт в целом?',
                             choices=(('5', 'Отлично'),
                                      ('4', 'Хорошо'),
                                      ('3', 'Могло быть лучше'),
                                      ('2', 'Плохо'),
                                      ('1', 'Ужасно')), initial=5)
    missect = forms.CharField(label='Какого раздела, на Ваш взгляд, не хватает?', min_length=3, max_length=100)
    howfind = forms.MultipleChoiceField(label='Откуда Вы узнали о нас?',
                             choices=(('1', 'От друзей/знакомых/родственников'),
                                      ('2', 'Из социальных сетей'),
                                      ('3', 'Из поисковых систем'),
                                      ('4', 'Другое')), widget=forms.CheckboxSelectMultiple, required=False)
    mind = forms.CharField(label='Ваш короткий отзыв или предложение по улучшению сайта:', min_length=2, max_length=2048,
                           widget=forms.Textarea(attrs={'rows':16, 'cols':128}), required=False)


class CommentForm(forms.ModelForm):
    """Comment form on 'blogpost.html' page."""
    class Meta:
        model = Comment                     # used model
        fields = ('text',)                  # only the 'text' field fill in required
        labels = {'text': "Комментарий"}    # form's 'text' field label


class BlogForm(forms.ModelForm):
    """New post form on 'newpost.html' page."""
    class Meta:
        model = Blog
        fields = ('title', 'image', 'description', 'content', 'author', 'posted',)
        labels = {
            'title':'Заголовок:',
            'image':'Изображение:',
            'description':'Краткое описание:',
            'content':'Текст статьи:',
            'author':'Автор:',
            'posted':'Дата:',
        }

