from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.urls')), 
    path('api/', include('exercise.urls')),  
    path('api/', include('meals.urls')),  
     path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
