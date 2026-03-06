from django.db import models
from config import settings

class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return f"Review by {self.author} for {self.movie.title}"