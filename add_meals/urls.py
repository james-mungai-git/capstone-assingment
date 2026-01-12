from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, FoodViewSet

router = DefaultRouter()
router.register(r'meal-items', MealViewSet, basename='meal')
router.register(r'food-items', FoodViewSet, basename='food')

urlpatterns = [
    path('', include(router.urls)),
]
