from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ]
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
        ]
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


class FoodItem(models.Model):
    food_name = models.CharField(max_length=100)

    def __str__(self):
        return self.food_name