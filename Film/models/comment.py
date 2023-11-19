from django.db import models

from django.contrib.auth.views import get_user_model
from Film.models import Movie

User = get_user_model()


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)