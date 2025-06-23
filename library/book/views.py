# book/views.py

from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse

from .models import Book
from .forms  import BookForm


@login_required
def book_list(request):
    title_query  = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()
    qs = Book.objects.all()
    if title_query:
        qs = qs.filter(name__icontains=title_query)
    if author_query:
        qs = qs.filter(authors__surname__icontains=author_query)
    qs = qs.distinct()
    return render(request, 'book/book_list.html', {
        'books': qs,
        'title_query': title_query,
        'author_query': author_query,
    })


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})


@login_required
def book_create(request):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # 1) создаём книгу без m2m
            book = form.save(commit=False)
            book.save()
            # 2) вручную привязываем выбранных авторов
            book.authors.set(form.cleaned_data['authors'])
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'book/book_form.html', {'form': form})


@login_required
def book_update(request, book_id):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # 1) сохраняем основные поля
            book = form.save(commit=False)
            book.save()
            # 2) обновляем m2m-связь авторов
            book.authors.set(form.cleaned_data['authors'])
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'book/book_form.html', {
        'form': form,
        'book': book,
    })


@login_required
def book_delete(request, book_id):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    book = get_object_or_404(Book, id=book_id)
    if book.order_set.exists():
        return HttpResponse("Cannot delete: book has active orders", status=400)
    book.delete()
    return redirect('book_list')
