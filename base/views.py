from django.shortcuts import render, redirect
from .forms import Register, UserProfileForm, BlogPostForm, MealForm, Exerciseform
from .models import UserProfile,  BlogPost,  Meal, Exercise
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as auth_logout
from datetime import date

# Home view
from django.shortcuts import render, redirect

def dashboard(request):
    today = date.today()

    breakfast_meals = Meal.objects.filter(user=request.user, name="Breakfast", date=today)
    lunch_meals = Meal.objects.filter(user=request.user, name="Lunch", date=today)
    dinner_meals = Meal.objects.filter(user=request.user, name="Dinner", date=today)

    breakfast_total = sum(item.calories() for item in breakfast_meals)
    lunch_total = sum(item.calories() for item in lunch_meals)
    dinner_total = sum(item.calories() for item in dinner_meals)

    return render(request, "base/dashboard.html", {
        "breakfast_total": breakfast_total,
        "lunch_total": lunch_total,
        "dinner_total": dinner_total,
    })
  
    
def logout(request):
    auth_logout(request)
    return redirect('/login/')

# Signup view
def signup(request):
    if request.method == "POST":
        form = Register(request.POST)  
        if form.is_valid():
            form.save()  
            return redirect('login')  
    else:
        form = Register()

    return render(request, 'base/registration/sign_up.html', {'form': form})

def userprofile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('user-profile')
    else:
        form = UserProfileForm()

    return render(request, 'base/user-profile.html', {'form': form})

# blogpost crud operations

class BlogPostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BlogPost
    template_name = "base/blog/blog-post.html"
    form_class = BlogPostForm
    success_url = reverse_lazy("blog-list")
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return True

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "base/blog/blog-detail.html"
    context_object_name = 'post'
    

class BlogPostListView(ListView):
    model = BlogPost
    template_name = "base/blog/blog-list.html"
    context_object_name = 'posts'
    ordering = ['-published_date']
    

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "base/blog/blog-delete.html"
    success_url = reverse_lazy("blog-list")  # usually list view

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author
   
            
        
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "content"]
    template_name = "base/blog/blog-post.html"
    success_url = reverse_lazy("blog-post")
    
    def test_func(self):
        post = self.get_object
        return self.request.author == post.author
    
# mealitem crud


class MealCreateView(CreateView):
    model = Meal
    template_name = "base/meal_item/add_meal.html"
    form_class = MealForm
    success_url = reverse_lazy ('dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date = date.today()
        return super().form_valid(form)
    
 
class MealUpdateView(UpdateView):
     model = Meal
     template_name = "base/meal_item/add_meal.html"
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
    template_name = "base/meal_item/meal-list.html"
    context_object_name = 'meals'

    def get_queryset(self):
        meal_type = self.kwargs.get('meal_type').capitalize() 
        return Meal.objects.filter(
            user=self.request.user,
            name=meal_type,
            date=date.today()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_type'] = self.kwargs.get('meal_type')
        
        breakfast_meals = Meal.objects.filter(user=self.request.user, name="Breakfast", date=date.today())
        lunch_meals = Meal.objects.filter(user=self.request.user, name="Lunch", date=date.today())
        dinner_meals = Meal.objects.filter(user=self.request.user, name="Dinner", date=date.today())

        context['breakfast_total'] = sum(item.calories() for item in breakfast_meals)
        context['lunch_total'] = sum(item.calories() for item in lunch_meals)
        context['dinner_total'] = sum(item.calories() for item in dinner_meals)

        return context
    
class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    template_name = "base/dashboard.html"
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
    template_name = "base/meal_item/meal-detail.html"
    
    def get_object(self, queryset =None):
        obj = super().get_object()
        
        if obj.user != self.request.user:
            raise PermissionDenied("you are not allowed to view this item")
        else:
            return obj 


class ExerciseCreateView(CreateView):
    model = Exercise
    form_class = Exerciseform
    template_name = "base/exercise/log_exercise.html"
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self,form):
        form.instance.author = self.request.author
        return super().form_valid()


class ExerciseListView(ListView):
    model = Exercise
    template_name = "base/exercise/exercise_list.html"
    context_object_name = 'exercises'
    


class ExerciseUpdateView(UpdateView):
    model = Exercise
    template_name = "base/exercise/log_exercise.html"
    success_url = reverse_lazy ("dashboard")
    
    def get_object(self,):
        obj = super().get_object()
        
        if obj.user != self.request.user:
            raise PermissionDenied("you are jot allowed to updatethis item")
        
        return obj
    

class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Exercise
    template_name = "base/exercise/delete-log.html"
    success_url = reverse_lazy ("dashboard")
    
    def get_object(self,):
        obj = super().get_object()
    
        if obj.user != self.request.user:
            raise PermissionDenied("you are jot allowed to delete this item")
        
        return obj
        
    def test_func(self):
        obj = self.get_object
        return self.request.user == obj.user

