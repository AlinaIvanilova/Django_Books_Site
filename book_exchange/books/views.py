from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Book, ExchangeProposal
from .forms import BookForm, ExchangeProposalForm

# 📚 Перегляд списку книг
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# ➕ Додавання книги (лише для авторизованих)
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

# 🔐 Реєстрація користувача
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'books/signup.html', {'form': form})

# 🔑 Вхід користувача
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'books/login.html', {'form': form})

# 🚪 Вихід користувача
def logout_view(request):
    logout(request)
    return redirect('book_list')

# 🔄 Пропозиція обміну книги
@login_required
def propose_exchange(request, book_id):
    requested_book = get_object_or_404(Book, id=book_id)

    # Не дозволяти обмінювати свої власні книги
    if requested_book.owner == request.user:
        return redirect('book_list')

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.from_user = request.user
            proposal.to_user = requested_book.owner
            proposal.requested_book = requested_book
            proposal.save()

            # ✅ Повідомлення про успішну відправку пропозиції
            messages.success(request, "Пропозиція обміну успішно надіслана!")

            return redirect('book_list')
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'books/propose_exchange.html', {
        'form': form,
        'requested_book': requested_book
    })

# 📜 Перегляд отриманих пропозицій
@login_required
def received_proposals(request):
    proposals = ExchangeProposal.objects.filter(to_user=request.user, status='pending')
    return render(request, 'books/received_proposals.html', {'proposals': proposals})

# ✅ Відповідь на пропозицію (прийняти або відхилити)
@login_required
def respond_to_proposal(request, proposal_id, action):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, to_user=request.user)

    if action == 'accept':
        proposal.status = 'accepted'
    elif action == 'reject':
        proposal.status = 'rejected'

    proposal.save()
    return redirect('received_proposals')
