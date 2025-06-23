from django.shortcuts import render, get_object_or_404
from .models import Book

def book_list(request):
    """
    Показывает каталог всех книг, с фильтрацией по названию и фамилии автора.
    """
    books = Book.objects.all()

    # Считываем параметры из строки запроса
    title_query  = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()

    if title_query:
        books = books.filter(name__icontains=title_query)
    if author_query:
        # Фильтруем по фамилии любого связанного автора
        books = books.filter(authors__surname__icontains=author_query)

    # Убираем дубликаты, если несколько авторов совпало
    books = books.distinct()

    return render(request, 'book/book_list.html', {
        'books': books,
        'title_query': title_query,
        'author_query': author_query,
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})
