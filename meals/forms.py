from django import forms
from .models import  Meal


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