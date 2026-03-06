from django.db import models

class Cast(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='casts')
    name = models.CharField(max_length=255)
    character = models.CharField(max_length=255)
    order = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} as {self.character}"