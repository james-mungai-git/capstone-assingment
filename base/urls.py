from django.urls import path
from . import views
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    logout,
    FoodItemListView,
    FoodItemDetailView,
    FoodItemCreateView,
    FoodItemUpdateView,
    FoodItemDeleteView,
    
    MealItemListView,
    MealItemDetailView,
    MealItemCreateView,
    MealItemUpdateView,
    MealItemDeleteView
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # blogcrud urls - use /blog/ prefix
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('blog/new/', BlogPostCreateView.as_view(), name='blog-post'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog-update'),

    # fooditem crud urls - use /food/ prefix
    path('food/', FoodItemListView.as_view(), name='food-list'),
    path('food/<int:pk>/', FoodItemDetailView.as_view(), name='food-detail'),
    path('food/new/', FoodItemCreateView.as_view(), name='food_item'),
    path('food/<int:pk>/edit/', FoodItemUpdateView.as_view(), name='food-update'),
    path('food/<int:pk>/delete/', FoodItemDeleteView.as_view(), name='food-delete'),
    
    # meal item crud 
    path('meal/',  MealItemListView.as_view(), name='home'),
    path('meal/<int:pk>/', MealItemDetailView.as_view(), name='meal-detail'),
    path('meal/new/', MealItemCreateView.as_view(), name='add_meal'),
    path('meal/<int:pk>/edit/', MealItemUpdateView.as_view(), name='update_meal'),
    path('meal/<int:pk>/delete/', MealItemDeleteView.as_view(), name='home'),
    
    
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='base/registration/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('user-profile/', views.userprofile, name = 'user-profile')
]
