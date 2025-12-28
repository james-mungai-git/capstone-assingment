from django.urls import path
from .views import (
    ExerciseCreateView,
    ExerciseDeleteView,
    ExerciseListView,
    ExerciseUpdateView,
)

urlpatterns = [
  
    path('exercise/',  ExerciseListView.as_view(), name='home'),
    path('exercise/new/', ExerciseCreateView.as_view(), name='log_exercise'),
    path('exercise/<int:pk>/edit/', ExerciseUpdateView.as_view(), name='update-exercise'),
    path('exercise/<int:pk>/delete/', ExerciseDeleteView.as_view(), name='home'),
    
    
  
]
