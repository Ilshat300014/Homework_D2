from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import *
from .forms import PostForms
from .models import Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from datetime import datetime

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-createDate']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('news:allNews')

@login_required
def sign_category(request, category_name, pk):
    user = request.user
    currentCategory = Category.objects.get(categoryName=category_name)
    if not user.category_set.filter(categoryName=category_name):
        currentCategory.subscribers.add(user)
    return redirect('news:postDetail', pk=pk)

class SearchNews(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'filter_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        # кэш очень похож на словарь, и метод get действует также.
        # Он забирает значение по ключу, если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = self.request.user
            categoryModel = self.object.category.get_queryset() # Получаем все категории поста
            category_names = []
            for c in categoryModel:
                if not user.category_set.filter(categoryName=c.categoryName).exists():
                    context['is_not_subscr'] = True
                    category_names.append(c.categoryName)
            context['category_names'] = category_names
            return context
        except:
            return context

class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = ('news.add_post',)
    template_name = 'postCreate.html'
    form_class = PostForms

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        author = request.POST['author']
        today = datetime.today().date()
        author_post_count = Post.objects.filter(author=author, createDate__date=today).count()
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            if author_post_count < 3:
                form.save()
                return redirect('news:allNews')
            else:
                return render(request, 'limit_error.html')


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'postCreate.html'
    form_class = PostForms

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    template_name = 'postDelete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:allNews')
