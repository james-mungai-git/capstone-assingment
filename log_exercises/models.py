from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
from django.contrib.auth.models import User
from django.db import models

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rep_name = models.CharField(max_length=100)  
    category = models.CharField(
        max_length=50,
        choices=[
            ('cardio', 'Cardio'),
            ('strength', 'Strength'),
            ('flexibility', 'Flexibility'),
            ('other', 'Other'),
        ],
        default='cardio'
    )
    date = models.DateField(default=date.today)
    time = models.TimeField(default=time(6, 0))  
    duration_minutes = models.PositiveIntegerField()  
    calories_burned = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.calories_burned}"

    