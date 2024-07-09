from django.urls import path
from .views import post_create, post_detail, user_posts, all_posts, posts_categories, doctors_list

urlpatterns = [
    path('post-new', post_create, name='post-new'),
    path('post-detail/<int:pk>/', post_detail, name='post-detail'),
    path('posts-categories/', posts_categories, name='posts-categories'),
    path('user-posts/', user_posts, name='user-posts'),
    path('all-posts/<int:pk>/', all_posts, name='all-posts'),
    path('doctors-list/', doctors_list, name='doctors-list'),
]