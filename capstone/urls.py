from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_accounts.urls')), 
    path('api/', include('log_exercises.urls')),  
    path('api/', include('add_meals.urls')),  
     path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
