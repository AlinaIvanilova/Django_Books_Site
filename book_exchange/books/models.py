from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} — {self.author}"