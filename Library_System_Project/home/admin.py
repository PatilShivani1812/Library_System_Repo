from django.contrib import admin
from .models import Book, Student, Transaction, Librarian
from datetime import timedelta, datetime

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'copies_available')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'date_borrowed', 'due_date', 'renewal_count')
    list_filter = ('student', 'book', 'due_date', 'renewal_count')
    actions = ['mark_borrowed', 'mark_returned']

    def mark_borrowed(self, request, queryset):
        queryset.update(date_borrowed=datetime.now().date())
    mark_borrowed.short_description = "Mark selected transactions as borrowed"

    def mark_returned(self, request, queryset):
        for transaction in queryset:
            transaction.book.copies_available += 1
            transaction.book.save()
            transaction.delete()
    mark_returned.short_description = "Mark selected transactions as returned"

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user',)