"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# Created by RickDalton:

# Модель данных блога
class Blog(models.Model):
    title = models.CharField(max_length = 128, unique_for_date = "posted", verbose_name = "Заголовок")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    # атрибуты null, blank в поле author обязательны для установки,
    # т.к. поле автор не заполнено у ранее сохраненных статей;
    # тип ForeignKey - так как у каждой статьи будет только один автор, но у автора может быть много статей
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, verbose_name = "Автор")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликовано")
    def get_absolute_url(self):                 # возвращает строку с уникальным URL записи
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self):                          # метод возвращает название, используемое для представления
        return self.title                       # отдельных записей в административном разделе
    # Внимание на отступ класса Meta: он должен быть вложен в основной класс Blog, иначе всё заданное в нём не применится
    class Meta:
        db_table = "Posts"                      # имя таблицы для модели
        ordering = ["-posted"]                  # порядок сортировки данныхв модели ("-" убывание)
        verbose_name = "статья блога"           # имя, под которым модель будет отобр. в админке (для одной статьи блога)
        verbose_name_plural = "статьи блога"    # то же, для всех статей блога



class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Добавлен")
    author = models.ForeignKey(User, null = True, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, null = True, on_delete = models.SET_NULL, verbose_name = "Статья")
    def __str__(self):
        return "Комментарий %s к %s" % (self.author, self.post)
    class Meta:
        db_table = "Comments"                   # имя таблицы для модели
        ordering = ["-date"]
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии к статьям блога"


admin.site.register(Blog)                       # регистрация модели после определения её классов - 
admin.site.register(Comment)                    #для возможности её редактирования в админке.
