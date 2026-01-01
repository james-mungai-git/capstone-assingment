
from .forms import  MealForm
from .models import   Meal, Food
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from datetime import date
from django.shortcuts import render


# Create your views here.
def dashboard(request):
    today = date.today()
    calorie_budget =1458
    
    if request.user.is_authenticated:
        breakfast_meals = Meal.objects.filter(user=request.user, name="Breakfast", date=today)
        lunch_meals = Meal.objects.filter(user=request.user, name="Lunch", date=today)
        dinner_meals = Meal.objects.filter(user=request.user, name="Dinner", date=today)

        breakfast_total = sum(item.calories() for item in breakfast_meals)
        lunch_total = sum(item.calories() for item in lunch_meals)
        dinner_total = sum(item.calories() for item in dinner_meals)
        
        total_consumed = breakfast_total+lunch_total+dinner_total
        calories_left = max(calorie_budget-total_consumed, 0)
    else:
      breakfast_total = lunch_total = dinner_total = total_consumed = 0
      calories_left = calorie_budget

    return render(request, "meals/dashboard.html", {
        "calorie_budget": calorie_budget,
        "calories_left": calories_left,
        "breakfast_total": breakfast_total,
        "lunch_total": lunch_total,
        "dinner_total": dinner_total,
    })
  
    
class MealCreateView(CreateView):
    model = Meal
    template_name = "meals/add_meal.html"
    form_class = MealForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date = date.today()

        food_name = form.cleaned_data['food']
        food_obj, created = Food.objects.get_or_create(name=food_name)
        form.instance.food = food_obj

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        
        if search:
            context['foods']=Food.objects.filter(name__icontaines=search)
        else:
            context['foods'] = Food.objects.none()
        return context
    
    def get_initial(self):
        initial =super().get_initial()
        food_id =self.request.GET.get('food_id')
        
        if food_id:
            try:
                food = Food.objects.get(id=food_id)
                initial['food']=food.name
                initial['calories_per_100g']=food.calories_per_100g
            except Food.DoesNotExist:
                pass

        return initial
    
class MealUpdateView(UpdateView):
     model = Meal
     template_name = "meals/add_meal.html"
     success_url =reverse_lazy ('dashboard')
     fields = ['name', 'food', 'quantity', 'calories_per_100g']  

     
     def get_object(self, queryset=None):
         obj = super().get_object(queryset)
         if obj.user != self.request.user:
             raise PermissionDenied("you are not allowed to uppdate this item")
         else:
            return obj


class MealListView(ListView):
    model = Meal
    template_name = "meals/meal-list.html"
    context_object_name = 'meals'
    
    def get_queryset(self):
        meal_type = self.kwargs.get('meal_type').capitalize()
        if not self.request.user.is_authenticated:
            return Meal.objects.none()

        queryset = Meal.objects.filter(
            user=self.request.user,
            date=date.today(),
            name=meal_type
        )

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(food__name__icontains=search)

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_type'] = self.kwargs.get('meal_type')

        if self.request.user.is_authenticated:
            breakfast_meals = Meal.objects.filter(user=self.request.user, name="Breakfast", date=date.today())
            lunch_meals = Meal.objects.filter(user=self.request.user, name="Lunch", date=date.today())
            dinner_meals = Meal.objects.filter(user=self.request.user, name="Dinner", date=date.today())

            context['breakfast_total'] = sum(item.calories() for item in breakfast_meals)
            context['lunch_total'] = sum(item.calories() for item in lunch_meals)
            context['dinner_total'] = sum(item.calories() for item in dinner_meals)
        else:
            context['breakfast_total'] = 0
            context['lunch_total'] = 0
            context['dinner_total'] = 0

        return context   
  
class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    template_name = "meals/dashboard.html"
    success_url = reverse_lazy('dashboard')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You are not allowed to delete this")
        return obj
    
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

       

class MealDetailView(DetailView):
    model = Meal
    template_name = "meals/meal-detail.html"
    
    def get_object(self, queryset =None):
        obj = super().get_object()
        
        if obj.user != self.request.user:
            raise PermissionDenied("you are not allowed to view this item")
        else:
            return obj 

class FoodListView(ListView):
    model = Food
    template_name = "meals/add_meal.html"
    context_object_name = "foods"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset