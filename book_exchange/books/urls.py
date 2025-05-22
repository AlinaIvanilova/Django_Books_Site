from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('book/<int:book_id>/update/', views.update_book, name='update_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('propose/<int:book_id>/', views.propose_exchange, name='propose_exchange'),
    path('received-proposals/', views.received_proposals, name='received_proposals'),
    path('respond_to_proposal/<int:proposal_id>/<str:action>/', views.respond_to_proposal, name='respond_to_proposal'),
]