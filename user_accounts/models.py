from django.db import models
from django.contrib.auth.models import User
from datetime import date, timezone
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

    
    def maintenance_calories(self):
        """Calculate daily maintenance calories (TDEE)."""
        if not self.weight or not self.height or not self.age:
            return None  

        if self.gender == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        activity_map = {
            'light': 1.2,
            'lightly_active': 1.375,
            'moderate': 1.55,
            'moderately_active': 1.725,
            'high': 1.9,
            'highly_active': 2.0, 
        }

        multiplier = activity_map.get(self.activity_level, 1.2)
        
        return int(bmr * multiplier)

    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
