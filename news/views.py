from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from django.shortcuts import render
from .filters import *
from .forms import PostForms

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-createDate']
    paginate_by = 10

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

class PostCreate(ListView):
    model = Post
    template_name = 'postCreate.html'
    context = 'postCreate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForms()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


