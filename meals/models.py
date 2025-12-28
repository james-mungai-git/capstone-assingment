from django.db import models
from django.contrib.auth.models import User
from datetime import date, timezone
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)        # "Breakfast", "Lunch", "Dinner"
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.now())
    food = models.CharField(max_length=200)
    quantity = models.FloatField()
    calories_per_100g = models.FloatField(default=0)
    
    def calories(self):
        return int (self.calories_per_100g * (self.quantity / 100))

    def __str__(self):
        return f"{self.name} ({self.food}) on {self.date}"