from django.db import models

# Create your models here.

class Product(models.Model):
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()

    def __str__(self):
        return self.title