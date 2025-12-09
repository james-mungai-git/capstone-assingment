from django.urls import path
from . import views
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='blog-list'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('posts/new/', BlogPostCreateView.as_view(), name='blog-post'),
    path('posts/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog-update'),
    path('posts/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),
    
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='base/registration/login.html'), name='login'),
    path('food_item/', views.FoodItem, name='food_item' ),
    path('user-profile/', views.userprofile, name = 'user-profile')
]
