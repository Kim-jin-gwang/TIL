from django.db import models
from .movie import Movie

class Genre(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name
