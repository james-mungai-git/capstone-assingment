from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,  BlogPost, Meal, Exercise

class Register(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model =  UserProfile
        fields = ["age", "weight", "height", "gender", "activity_level"]
        
        
class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'content')
from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'food', 'quantity', 'calories_per_100g']  

        widgets = {
            'name': forms.Select(choices=[
                ('Breakfast', 'Breakfast'),
                ('Lunch', 'Lunch'),
                ('Dinner', 'Dinner'),
            ]),
            'food': forms.TextInput(attrs={'placeholder': 'Enter food name'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantity in grams'}),
            'calories_per_100g': forms.NumberInput(attrs={'placeholder': 'Calories per 100g'}),
        }
class Exerciseform(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["rep_name", "category","duration_minutes", "calories_burned" ]
        