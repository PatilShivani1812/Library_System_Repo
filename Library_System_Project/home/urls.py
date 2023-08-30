from django.urls import path
from . import views

urlpatterns = [
    path('available-books/', views.available_books, name='available_books'),
    path('borrowed-books/', views.borrowed_books, name='borrowed_books'),
    path('renew-book/<int:transaction_id>/', views.renew_book, name='renew_book'),
    path('borrow-book/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return-book/<int:transaction_id>/', views.return_book, name='return_book'),
    path('', views.librarian_dashboard, name='librarian_dashboard'),
    path('mark-borrowed/<int:transaction_id>/', views.mark_borrowed, name='mark_borrowed'),
    path('mark-returned/<int:transaction_id>/', views.mark_returned, name='mark_returned'),
]
