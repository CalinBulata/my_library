from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
import random

from loans.models import Book
from loans.forms import BookForm

from my_library import settings

ITEMS_PER_PAGE =25

def welcome(request):
    slogans = ["Having fun isn't hard when you've got a library card.",
                "Libraries make shhh happen.", 
                "Believe in your shelf.", 
                "Need a good read? We've got you covered.", 
                "Check us out. And maybe one of our books too.", "Get a better read on the world"]
    context = {'slogan': random.choice(slogans)}
    return render(request, 'welcome.html', context)

def list_books(request):
    book_list = Book.objects.all().order_by('id')
    paginator = Paginator(book_list, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    context = {'page_object': page_object}
    return render(request, 'books.html', context)

def get_book(request, book_id):
    try:
        context = {'book': Book.objects.get(pk=book_id)}
    except Book.DoesNotExist:
        raise Http404(f"Could not find book with primary key {book_id}")
    else:
        return render(request, 'get_book.html', context)
    
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "It was not possible to save this book to the database.")
            else:
                path = reverse('list_books')
                return HttpResponseRedirect(path)
    else:
        form = BookForm()
    return render(request, 'create_book.html', {'form': form})

def update_book(request, book_id):
    try:
        Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404(f"Could not find book with primary key {book_id}")
    if request.method == "POST":
        book = Book.objects.get(pk=book_id)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                book = form.save()
            except:
                form.add_error(None, "It was not possible to update this book in the database.")
            else:
                messages.info(request, f"Updated book record to: {book}")
                path = reverse('list_books')
                return HttpResponseRedirect(path)
    else:
        book = Book.objects.get(pk=book_id)
        form = BookForm(instance=book)
    return render(request, 'update_book.html', {'form': form, 'book': book})

def delete_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404(f"Could not find book with primary key {book_id}")
    if request.method == "POST":
        book.delete()
        path = reverse('list_books')
        return HttpResponseRedirect(path)
    return render(request, 'delete_book.html', {'book': book})