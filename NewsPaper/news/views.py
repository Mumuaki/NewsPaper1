from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем обратную сортировку по полю дата создания
    ordering = '-created_at'
    # Используем другой шаблон — product.html
    template_name = 'post_id.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
