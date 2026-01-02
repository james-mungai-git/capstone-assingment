from rest_framework import viewsets, permissions
from .models import Meal, Food
from .serializers import MealSerializer, FoodSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date
from django.core.paginator import Paginator, EmptyPage

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Meal.objects.filter(user=self.request.user).order_by('-date', '-time')
      

        meal_type = self.request.query_params.get('meal_type')
        if meal_type:
            queryset = queryset.filter(name__iexact=meal_type)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        perpage = int(self.request.GET.get('perpage', 3))
        page = int(self.request.GET.get('page', 1))
        search = self.request.GET.get('search', '')
        queryset=self.get_queryset
        if search:
            queryset= queryset.filter(name__icontains=search)
        
        paginator = Paginator(queryset, per_page=perpage)
        
        try:
            paginated_queryset = paginator.page(page)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)
            
        context['paginated_queryset'] = paginated_queryset
        context['search'] = search
        context['perpage'] = perpage
        context['page'] = page

        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        limit = int(self.request.GET.get('limit'))
        items = Meal.objects.all()[:limit]
        
        data = [
            {
                'id':items.id, 
                'user':items.user, 
                'name':items.name,
                'date':items.date, 
                'time':items.time, 
                'food':items.food, 
                'food_id':items.food_id, 
                'quantity':items.quantity, 
                'calories':items.calories
            }
        ]
        
        

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
            calories = meal.calories()
            meal_type = meal.name.capitalize()
            if meal_type in summary:
                summary[meal_type] += calories
            summary['Total'] += calories

        return Response(summary)
