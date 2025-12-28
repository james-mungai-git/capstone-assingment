from django.urls import path
from .views import (
     MealListView,
    MealDetailView,
    MealCreateView,
    MealUpdateView,
    MealDeleteView,
)
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('meal/<str:meal_type>',  MealListView.as_view(), name='meal-list'),
    path('meal/<int:pk>/', MealDetailView.as_view(), name='meal-detail'),
    path('meal/new/', MealCreateView.as_view(), name='add_meal'),
    path('meal/<int:pk>/edit/', MealUpdateView.as_view(), name='update_meal'),
    path('meal/<int:pk>/delete/', MealDeleteView.as_view(), name='home'),
    
  
]
