from django import forms
from .models import Book, ExchangeProposal

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'image', 'description']

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['offered_book']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Отримується з view
        super().__init__(*args, **kwargs)
        self.fields['offered_book'].queryset = Book.objects.filter(owner=user)
        self.fields['offered_book'].label = "Оберіть одну зі своїх книг для обміну"
