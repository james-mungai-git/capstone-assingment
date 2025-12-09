from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, FoodItem

class Register(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model =  UserProfile
        fields = ["age", "weight", "height", "gender", "activity_level"]