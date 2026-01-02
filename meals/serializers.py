from rest_framework import serializers
from .models import Food, Meal
from django.contrib.auth import get_user_model

User = get_user_model()



class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'calories_per_100g']



class MealSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    food = FoodSerializer()
    calories = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'user', 'name', 'date', 'time', 'food', 'food_id', 'quantity', 'calories']

    def get_calories(self, obj):
        return obj.calories()
