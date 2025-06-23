from django.shortcuts            import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                 import HttpResponse
from .models                     import Author

@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author/author_list.html', {'authors': authors})

@login_required
def author_create(request):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    error = None
    if request.method == 'POST':
        name       = request.POST.get('name', '').strip()
        surname    = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip() or None

        if name and surname:
            a = Author.create(name=name, surname=surname, patronymic=patronymic)
            if a:
                return redirect('author_list')
            else:
                error = "Invalid data"
        else:
            error = "Name and surname are required"

    return render(request, 'author/author_form.html', {'error': error})

@login_required
def author_delete(request, author_id):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    author = get_object_or_404(Author, id=author_id)
    if author.books.exists():
        return HttpResponse("Cannot delete: author has books", status=400)

    author.delete()
    return redirect('author_list')

@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books  = author.books.all() 
    return render(request, 'author/author_detail.html', {
        'author': author,
        'books':  books,
    })
