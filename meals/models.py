from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories_per_100g = models.FloatField()

    def __str__(self):
        return self.name

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.now)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)  
    quantity = models.FloatField()  

    def calories(self):
        return int(self.food.calories_per_100g * (self.quantity / 100))

    def __str__(self):
        return f"{self.name} ({self.food.name}) on {self.date}"