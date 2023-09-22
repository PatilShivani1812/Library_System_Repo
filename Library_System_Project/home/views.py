from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from .models import Book, Student, Transaction, Librarian
from django.utils import timezone

# Create your views here.

def available_books(request):
    """
    Retrieves a list of all available books from the database and 
    renders them in the 'available_books.html' template.
    """
    books = Book.objects.all()
    return render(request, 'available_books.html', {'books': books})

@login_required
def borrowed_books(request):
    """
    Renders a list of books borrowed by the currently logged-in 
    student user in the 'borrowed_books.html' template.
    """
    student = request.user.student
    transactions = Transaction.objects.filter(student=student)
   
    return render(request, 'borrowed_books.html', {'transactions': transactions})



@login_required
def renew_book(request, transaction_id):
    """
    Allows a student to renew a borrowed book if renewal conditions are met.

    Note:
    - Renewal conditions might include factors like whether the book has already 
    been renewed before, and whether it's overdue.
    """
    transaction = Transaction.objects.get(pk=transaction_id)
    if transaction.renewal_count < 1 and transaction.is_due():
        transaction.renewal_count += 1
        transaction.due_date = timezone.now().date() + timedelta(days=30)
        transaction.save()
        print("Renewal count:", transaction.renewal_count)
        print("Due date after renewal:", transaction.due_date)
    return redirect('borrowed_books')


@login_required
def borrow_book(request, book_id):

    """
    Allows a student to borrow a book if borrowing conditions are met.

    It takes a 'book_id' parameter to identify the specific book to be borrowed.
    The function first fetches the currently logged-in student's information from the 'request.user' object.
    It also fetches the book from the database using the provided 'book_id'.

    If the book has available copies and the student hasn't borrowed
    the maximum allowed number of books (10), a new Transaction object is created to represent the borrowing.
    The due date is set to the current date plus 30 days. The 'copies_available' count for the book is reduced by 1,
    and the book information is updated in the database.

    Note:
    - Borrowing conditions might include factors like the number of available copies of the book and the student's borrowing limit.
    """
    student = request.user.student
    book = Book.objects.get(pk=book_id)
    if book.copies_available > 0 and student.borrowed_books.count() < 10:
        transaction = Transaction.objects.create(book=book, student=student,
                                                due_date=datetime.now().date() + timedelta(days=30))
        book.copies_available -= 1
        book.save()
    return redirect('available_books')

@login_required
def return_book(request, transaction_id):
    """
    Allows a student to return a borrowed book.

    It takes a 'transaction_id' parameter to identify the specific book loan transaction to be returned.
    The function fetches the transaction and the associated book from the database using the provided 'transaction_id'.
    
    Upon returning the book, the available copies count for the book is incremented by 1 and the book information is updated.
    The transaction representing the loan is then deleted from the database.
    """

    transaction = Transaction.objects.get(pk=transaction_id)
    book = transaction.book
    book.copies_available += 1
    book.save()
    transaction.delete()
    return redirect('borrowed_books')

@login_required
def librarian_dashboard(request):
    """
    Renders a dashboard for librarians to view all transactions or redirects to available books page.

    If the logged-in user is a librarian, renders the 'librarian_dashboard.html' template with a list of transactions.
    Otherwise, redirects to the 'available_books' page.

    If the user is a librarian, all transactions are fetched from the Transaction model and passed to the template
    'librarian_dashboard.html' for rendering. Librarians can view all transactions.
    """
    if request.user.librarian:
        transactions = Transaction.objects.all()
        return render(request, 'librarian_dashboard.html', {'transactions': transactions})
    return redirect('available_books')

@login_required
def mark_borrowed(request, transaction_id):
    """
    Allows a librarian to mark a book as borrowed in a transaction.

    If the logged-in user is a librarian, the function fetches the transaction from the database using the provided 'transaction_id'.
    It updates the 'date_borrowed' field of the transaction with the current date and saves the updated transaction.
    
    Finally, the function redirects the librarian to the 'librarian_dashboard' page, where they can manage transactions.
    """
    if request.user.librarian:
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction.date_borrowed = datetime.now().date()
        transaction.save()
    return redirect('librarian_dashboard')




@login_required
def mark_returned(request, transaction_id):
    """
    Allows a librarian to mark a book as returned in a transaction.

    If the logged-in user is a librarian, the function fetches the transaction and the associated book from the database
    using the provided 'transaction_id'. It increments the available copies count for the book by 1 and updates the book information.
    The transaction representing the loan is then deleted from the database.
    
    Finally, the function redirects the librarian to the 'librarian_dashboard' page, where they can manage transactions.
    """

    
    if request.user.librarian:
        transaction = Transaction.objects.get(pk=transaction_id)
        book = transaction.book
        book.copies_available += 1
        book.save()
        transaction.delete()
    return redirect('librarian_dashboard')


#Hello views
