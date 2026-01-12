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
    food = serializers.CharField(write_only=True)
    calories = serializers.SerializerMethodField()
    food_id = serializers.ReadOnlyField(source='food.id')
    date = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()

    class Meta:
        model = Meal
        fields = [
            'id', 
            'user', 
            'name', 
            'food', 
            'food_id', 
            'quantity_in_grams', 
            'calories', 
            'date', 
            'time'
        ]

    def get_calories(self, obj):
        return obj.calories()

    def create(self, validated_data):
        food_name = validated_data.pop('food')
        try:
            food_instance = Food.objects.get(name__iexact=food_name)
        except Food.DoesNotExist:
            raise serializers.ValidationError(
                f"Food '{food_name}' does not exist."
            )

        meal = Meal.objects.create(food=food_instance, **validated_data)
        return meal
