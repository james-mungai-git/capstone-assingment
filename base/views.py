from django.shortcuts import render, redirect
from .forms import Register, UserProfileForm, BlogPostForm, MealItemForm, MealForm, Exerciseform
from .models import UserProfile, FoodItem, BlogPost, MealItem, Meal, Exercise
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as auth_logout
from .forms import FoodItemForm
from django.contrib.postgres.search import SearchVector


# Home view
def home(request):
    return render(request, 'base/home.html')

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
    



# food item crud operations 


class FoodItemCreateView(CreateView):
    model = FoodItem
    template_name = "base/food/food_item.html"
    form_class = FoodItemForm  
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
     
        form.instance.user = self.request.user  
        return super().form_valid(form)


class FoodItemListView(ListView):
    model = FoodItem
    template_name = "base/food/food-list.html"
    context_object_name = 'foods'
    
    def get_queryset(self):
        return FoodItem.objects.filter(user=self.request.user)


class FoodItemDetailView(DetailView):
    model = FoodItem
    template_name = "base/food/food-detail.html"
    context_object_name = 'food'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to view this food item")
        return obj


class FoodItemUpdateView(UpdateView):
    model = FoodItem
    template_name = "base/food/food-list.html"
    form_class = FoodItemForm  
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You can only edit your own food items")
        return obj


class FoodItemDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = FoodItem
    template_name = "base/food/food-delete.html"  
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You can only delete your own food items")
        return obj
    
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

# mealitem crud


class MealCreateView(CreateView):
    model = Meal
    template_name = "base/meal_item/add_meal.html"
    form_class = MealForm
    success_url = reverse_lazy ('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
 
class MealUpdateView(UpdateView):
     model = Meal
     template_name = "base/meal_item/update_meal.html"
     success_url =reverse_lazy ('home')
     fields = ['name','date', 'time', 'foods']

     
     def get_object(self, queryset=None):
         obj = super().get_object(queryset)
         if obj.user != self.request.user:
             raise PermissionDenied("you are not allowed to uppdate this item")
         else:
            return obj


class MealListView(ListView):
    model = Meal
    template_name = "base/meal_item/home.html"
    context_object_name = 'meals'
    
    def get_queryset(self):
        return MealItem.objects.filter(user=self.request.user)

class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    template_name = "base/home.html"
    success_url = reverse_lazy('home')
    
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
