from rest_framework import serializers
from .models import Exercise
from django.contrib.auth import get_user_model

User = get_user_model()


class ExerciseSerializer(serializers.ModelSerializer):
    # Show the username instead of user ID
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Exercise
        fields = [
            'id',
            'user',
            'rep_name',
            'category',
            'date',
            'time',
            'duration_minutes',
            'calories_burned',
        ]
