from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
# импортируем класс ListView, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
# импортируем класс DetailView получения деталей объекта
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.models import User
from datetime import datetime

from .models import Author, Category, Post, PostCategory, Comment
from .filters import PostFilter   # импортируем недавно написанный фильтр
from .forms import PostForm  # импортируем нашу форму

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.contrib.auth.mixins import PermissionRequiredMixin

# class MyView(PermissionRequiredMixin, View):
#     permission_required = ('<app>.<action>_<model>',
#                            '<app>.<action>_<model>')
#
#
# class AddProduct(PermissionRequiredMixin, CreateView):
#     permission_required = ('shop.add_product', )
#     #// customize form view

# class ProtectedView(LoginRequiredMixin, TemplateView):
#     template_name = 'protected_page.html'

# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    permission_required = ('news.change_post',)
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-pubDate']  # вывод списка публикаций в обратном порядке, от более новых к более старым
    paginate_by = 10  # поставим постраничный вывод в один элемент


    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['news_list'] = Post.objects.all()  # добавим переменную всего списка публикаций, не подверженного эффекту пагинации
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post',)
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST


# дженерик для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    permission_required = ('news.delete_post',)
    queryset = Post.objects.all()
    success_url = '/news/'



class SearchList(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    ordering = ['-pubDate']
    paginate_by = 10  # поставим постраничный вывод в 10 элементов

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['news_list'] = Post.objects.all()  # добавим переменную всего списка публикаций, не подверженного эффекту пагинации
        context['filter'] = self.get_filter()
        context['categories'] = Category.objects.all()
        return context


# создаём представление, в котором будут детали конкретного отдельного товара
# class PostDetail(DetailView):
#     model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного поста
#     template_name = 'new.html'  # название шаблона будет new.html
#     context_object_name = 'new'  # название объекта. в нём будет
#
#     # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
#         return context

