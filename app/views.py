"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import PollForm, BlogForm
# Imports the 'User' model to use the model in which data about users is stored:
# from django.contrib.auth.models import User 
# Registration form object transfer from the controller to the view:
from django.contrib.auth.forms import UserCreationForm
# Imports the 'Blog' model:
from django.db import models
from .models import Blog
# Using the comment model:
from .models import Comment
# Using the comment input form:
from .forms import CommentForm

def registration(request):
    """Renders the registration page."""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform':regform,
            'year':datetime.now().year
        }
    )


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    last_post = Blog.objects.first()
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'last_post': last_post,
            'year':datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )


def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Ссылки на полезные сайты.',
            'year':datetime.now().year,
        }
    )


def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужской', '2': 'Женский'}
    conven = {'1': 'Плохое', '2': 'Сильно запутанное', '3': 'Могло быть лучше', '4': 'Интуитивно понятное', '5': 'Идеальное'}
    mark = {'1': 'Ужасно', '2': 'Плохо', '3': 'Могло быть лучше', '4': 'Хорошо', '5': 'Отлично'}
    howfind = ['Друзья/знакомые/родственники', 'Социальные сети', 'Поисковые системы', 'Другое']
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['age'] = form.cleaned_data['age']
            data['conven'] = conven[ form.cleaned_data['conven'] ]
            data['mark'] = mark[ form.cleaned_data['mark'] ]
            data['missect'] = form.cleaned_data['missect']
            data['howfind'] = ''
            for i in form.cleaned_data['howfind']:
                if not data['howfind']:
                    data['howfind'] += howfind[ int(i) - 1 ]
                else:
                    data['howfind'] += ', ' + howfind[ int(i) - 1 ]
            data['mind'] = form.cleaned_data['mind']
            form = None
    else:
        form = PollForm()
    return render(
        request,
        'app/pool.html',
        {
            'data': data,
            'form': form,
            'title':'Опрос',
            'message':'Помогите нам сделать наш сайт лучше!',
            'year':datetime.now().year,
        }
    )


def blog(request):
    """Renders the blog page"""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()                              # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """renders the blogpost page"""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)                  # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)        # запрос на выбор всех комментариев выбранной статьи
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user                 # добавляем (т.к. этого поля нет в форме) в модель Комментария
                                                            #(Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now()                 # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr)  # добавляем в модель Comment статью, для которой данный комментарий
            comment_f.save()                                # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm()                                # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,                               # передача конкретной статьи в шаблон веб-страницы
            'comments': comments,                           # передача всех комментов к данной статье в шаблон веб-страницы
            'form': form,                                   # передача формы добавления коммента в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Создание новой статьи',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Видео по теме сайта.',
            'year':datetime.now().year,
        }
    )