from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    copies_available = models.PositiveIntegerField(default=0)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    borrowed_books = models.ManyToManyField(Book, through='Transaction')
    
class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    renewal_count = models.PositiveIntegerField(default=0)
    
    def is_due(self):
        return self.due_date < datetime.now().date()

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
