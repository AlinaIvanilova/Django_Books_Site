from django import forms
from .models import Book, ExchangeProposal

# Форма
class BookForm(forms.ModelForm):
    class Meta:
        model = Book  # Пов’язана модель — Book
        fields = ['title', 'author', 'image', 'description', 'category']

# Форма для створення пропозиції обміну
class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal  # Пов’язана модель — ExchangeProposal
        fields = ['offered_book']  # У формі буде лише поле вибору запропонованої книги

    def __init__(self, *args, **kwargs):
        # Отримуємо користувача з аргументів (очікується, що він буде переданий з view)
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Обмежуємо вибір книг лише тими, що належать поточному користувачу
        self.fields['offered_book'].queryset = Book.objects.filter(owner=user)

        # Задаємо зрозумілу мітку для поля
        self.fields['offered_book'].label = "Оберіть одну зі своїх книг для обміну"
