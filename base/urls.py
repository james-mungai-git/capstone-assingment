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
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth  import views as auth_views
urlpatterns = [
    # blogcrud urls 
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('blog/new/', BlogPostCreateView.as_view(), name='blog-post'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog-update'),
    
   

    path('sign-up/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='base/registration/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('user-profile/', views.userprofile, name = 'user-profile'),
    
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='base/registration/reset_password.html'),
         name='reset_password'),
    path('confirm_email/', 
         auth_views.PasswordResetDoneView.as_view(template_name='base/registration/confirm_email.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='base/registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('change-password/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='base/registration/change_password.html'), 
         name='password_reset_complete')
    
]
