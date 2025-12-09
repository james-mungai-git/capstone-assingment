from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='base/registration/login.html'), name='login'),
    path('food_item/', views.FoodItem, name='food_item' ),
    path('user-profile/', views.userprofile, name = 'user-profile')
]
