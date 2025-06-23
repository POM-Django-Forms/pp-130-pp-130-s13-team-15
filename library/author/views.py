from django.shortcuts            import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                 import HttpResponse
from .models                     import Author
from .forms                      import AuthorForm

@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author/author_list.html', {'authors': authors})

@login_required
def author_create(request):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()

    return render(request, 'author/author_form.html', {'form': form})

@login_required
def author_update(request, author_id):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    author = get_object_or_404(Author, id=author_id)

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_detail', author_id=author.id)
    else:
        form = AuthorForm(instance=author)

    return render(request, 'author/author_form.html', {
        'form': form,
        'author': author,
    })

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
