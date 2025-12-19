from django.urls import path
from . import views
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
 
    MealListView,
    MealDetailView,
    MealCreateView,
    MealUpdateView,
    MealDeleteView,
    
    ExerciseCreateView,
    ExerciseDeleteView,
    ExerciseListView,
    ExerciseUpdateView,
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # blogcrud urls 
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('blog/new/', BlogPostCreateView.as_view(), name='blog-post'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog-update'),
    
    # meal item crud 
    path('meal/<str:meal_type>',  MealListView.as_view(), name='meal-list'),
    path('meal/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('meal/new/', MealCreateView.as_view(), name='add_meal'),
    path('meal/<int:pk>/edit/', MealUpdateView.as_view(), name='update_meal'),
    path('meal/<int:pk>/delete/', MealDeleteView.as_view(), name='home'),
    
    path('exercise/',  ExerciseListView.as_view(), name='home'),
    path('exercise/new/', ExerciseCreateView.as_view(), name='log_exercise'),
    path('exercise/<int:pk>/edit/', ExerciseUpdateView.as_view(), name='update-exercise'),
    path('exercise/<int:pk>/delete/', ExerciseDeleteView.as_view(), name='home'),
    
    
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sign-up/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='base/registration/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('user-profile/', views.userprofile, name = 'user-profile')
]
