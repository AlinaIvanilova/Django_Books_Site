from django.db import models
from django.contrib.auth.models import User

# Модель книги
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_exchanged = models.BooleanField(default=False)  # Прапорець, чи вже обміняна книга

    def __str__(self):
        # Строкове представлення книги: назва і автор
        return f"{self.title} — {self.author}"

# Модель пропозиції обміну книгами
class ExchangeProposal(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_proposals', on_delete=models.CASCADE)  # Користувач, який пропонує обмін
    to_user = models.ForeignKey(User, related_name='received_proposals', on_delete=models.CASCADE)  # Користувач, якому запропоновано обмін
    offered_book = models.ForeignKey(Book, related_name='offered_in', on_delete=models.CASCADE)  # Книга, яку пропонують
    requested_book = models.ForeignKey(Book, related_name='requested_in', on_delete=models.CASCADE)  # Книга, яку хочуть отримати

    # Варіанти статусів обміну
    STATUS_CHOICES = [
        ('pending', 'Очікує'),    # Пропозиція очікує відповіді
        ('accepted', 'Прийнято'), # Пропозицію прийнято
        ('rejected', 'Відхилено'),# Пропозицію відхилено
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Статус пропозиції
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення пропозиції

    def __str__(self):
        # Строкове представлення пропозиції обміну
        return f"{self.from_user} пропонує {self.offered_book} за {self.requested_book}"
