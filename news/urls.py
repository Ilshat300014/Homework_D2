from django.urls import path, include
from .views import *

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view(), name='allNews'),
    path('<int:pk>/', PostDetail.as_view(), name='postDetail'),
    path('search/', SearchNews.as_view(), name='postSearch'),
    path('create/', PostCreate.as_view(), name='postCreate')
]