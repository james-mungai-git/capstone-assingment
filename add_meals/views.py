from rest_framework import viewsets, permissions
from .models import Meal, Food
from .serializers import MealSerializer, FoodSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'perpage'
    max_page_size = 50
    page_query_param = 'page'


class FoodViewSet(viewsets.ModelViewSet):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Food.objects.all()
        search = self.request.query_params.get('search', '')

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Meal.objects.filter(user=self.request.user).order_by('-date', '-time')

        meal_type = self.request.query_params.get('meal_type')
        if meal_type:
            queryset = queryset.filter(name__iexact=meal_type)

        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise permissions.PermissionDenied("You cannot update this meal")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You cannot delete this meal")
        instance.delete()

    @action(detail=False, methods=['get'])
    def today_summary(self, request):
        today = date.today()
        meals_today = Meal.objects.filter(user=request.user, date=today)
        summary = {'Breakfast': 0, 'Lunch': 0, 'Dinner': 0, 'Total': 0}

        for meal in meals_today:
            calories = meal.calories() if hasattr(meal, 'calories') else 0
            meal_type = meal.name.capitalize()
            if meal_type in summary:
                summary[meal_type] += calories
            summary['Total'] += calories

        return Response(summary)
