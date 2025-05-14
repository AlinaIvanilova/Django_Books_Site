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

class ExchangeProposal(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_proposals', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_proposals', on_delete=models.CASCADE)
    offered_book = models.ForeignKey(Book, related_name='offered_in', on_delete=models.CASCADE)
    requested_book = models.ForeignKey(Book, related_name='requested_in', on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('accepted', 'Прийнято'),
        ('rejected', 'Відхилено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} пропонує {self.offered_book} за {self.requested_book}"
