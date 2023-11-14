from datetime import date
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from Film.models import Actor, Movie


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'birthdate', 'gender')

    def validate_source(self, value):
        if value > date(1950, 1, 1):
            raise ValidationError(detail="Birthdate must be on or before January 1, 1950")
        return value


class MovieSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
