from django import forms
from .models import Exercise


class Exerciseform(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["rep_name", "category","duration_minutes", "calories_burned" ]
        