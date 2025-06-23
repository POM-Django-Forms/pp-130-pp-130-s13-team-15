from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from django.utils                   import timezone
from datetime                       import timedelta

from .models import Order
from .forms  import OrderForm

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            books = form.cleaned_data['books']
            if books:
                order.book = books[0]
            order.save()
            order.books.set(books)
            return redirect('my_orders')
    else:
        default_due = timezone.now().date() + timedelta(days=30)
        initial = {'plated_end_at': default_due}
        book_pk = request.GET.get('book')
        if book_pk:
            initial['books'] = [book_pk]
        form = OrderForm(initial=initial)

    return render(request, 'order/order_form.html', {'form': form})

@login_required
def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.role != 1 and order.user != request.user:
        return HttpResponse("Access denied", status=403)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            books = form.cleaned_data['books']
            if books:
                order.book = books[0]
            order.save()
            order.books.set(books)
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order/order_form.html', {'form': form, 'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('books')
    return render(request, 'order/my_orders.html', {'orders': orders})

@login_required
def order_list(request):
    orders = Order.objects.select_related('user').prefetch_related('books').order_by('-created_at')
    return render(request, 'order/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    can_close = order.end_at is None and (request.user.role == 1 or order.user == request.user)
    return render(request, 'order/order_detail.html', {'order': order, 'can_close': can_close})

@login_required
def close_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.end_at or request.method != 'POST':
        return HttpResponse(status=400)
    order.end_at = timezone.now()
    order.save()
    return redirect('order_detail', order_id=order.id)
