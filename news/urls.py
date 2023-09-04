from django.urls import path, include
from .views import *

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view(), name='allNews'),
    path('<int:pk>/', PostDetail.as_view(), name='postDetail'),
    path('search/', SearchNews.as_view(), name='postSearch'),
    path('add/', PostCreate.as_view(), name='postCreate'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='postUpdate'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='postDelete'),
    path('upgrade/', upgrade_me, name='upgrade')
]