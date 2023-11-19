from datetime import date
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Actor, Movie, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'birthdate', 'gender')  # Make sure 'birthdate' is a valid field in the 'Actor' model

    def validate_birthdate(self, value):
        if value < date(1950, 1, 1):
            raise ValidationError(detail="Birthdate must be on or before January 1, 1950")
        return value


class MovieSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class ADDActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name', 'birthdate', 'gender')  # Make sure 'birthdate' is a valid field in the 'Actor' model

    def validate_birthdate(self, value):
        if value < date(1950, 1, 1):
            raise ValidationError(detail="Birthdate must be on or before January 1, 1950")
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ("movie_id", "user_id", "text", "created_at")
