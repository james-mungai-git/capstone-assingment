from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, FoodItem, BlogPost, Meal, MealItem, Exercise

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
class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        
        fields = ['name','date', 'time', 'foods']
        widgets = {
            'foods': forms.CheckboxSelectMultiple()
        }


class MealItemForm(forms.ModelForm):
    class Meta:

        model = MealItem
        fields = ['meal', 'food', 'quantity']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'user', 'calories_per_100g']

class Exerciseform(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["rep_name", "category","duration_minutes", "calories_burned" ]
        