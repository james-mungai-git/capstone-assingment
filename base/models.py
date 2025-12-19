from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        default='male'  
    )

    activity_level = models.CharField(
        max_length=100,
        choices=[
            ('light', 'Light'),
            ('lightly_active', 'Lightly Active'),
            ('moderate', 'Moderate'),
            ('moderately_active', 'Moderately Active'),
            ('high', 'High'),
            ('highly_active', 'Highly Active'),
        ],
        default='light'  
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
    
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)        # "Breakfast", "Lunch", "Dinner"
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.now)
    food = models.CharField(max_length=200)
    quantity = models.FloatField()
    calories_per_100g = models.FloatField(default=0)
    
    def calories(self):
        return int (self.calories_per_100g * (self.quantity / 100))

    def __str__(self):
        return f"{self.name} ({self.food}) on {self.date}"

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

    