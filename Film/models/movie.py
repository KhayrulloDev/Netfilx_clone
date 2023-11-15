from django.db import models


class Movie(models.Model):
    actor = models.ManyToManyField('Actor')
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    imdb = models.FloatField()
    genre = models.CharField(max_length=50)
