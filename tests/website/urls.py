from django.urls import path, include
from django.contrib import admin
from django.views.generic import ListView, DetailView, View
from tests.blog.models import Post
from tests.blog.views import addPost, addComment


urlpatterns = [
    path('', ListView.as_view(model=Post, ordering='-pk'), name='index'),
    path('add-post', addPost, name='add_post'),
    path('<int:pk>/', DetailView.as_view(model=Post), name='post'),
    path('<int:pk>/add-comment', addComment, name='add_comment'),
]
