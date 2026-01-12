from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_accounts.views import BlogPostViewSet, UserProfileViewSet, RegisterViewSet, LoginViewSet
from log_exercises.views import ExerciseViewSet
from add_meals.views import MealViewSet, FoodViewSet
from rest_framework.authtoken.views import obtain_auth_token  

router = DefaultRouter()
router.register(r'blogposts', BlogPostViewSet, basename='blogpost')
router.register(r'userprofile', UserProfileViewSet, basename='userprofile')
router.register(r'exercise', ExerciseViewSet, basename='exercise')
router.register(r'meal-items', MealViewSet, basename='meal')
router.register(r'food-items', FoodViewSet, basename='food')

urlpatterns = [
    path('', include(router.urls)),  
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('auth-token/', obtain_auth_token),
]
