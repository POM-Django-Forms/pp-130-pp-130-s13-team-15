from datetime import timedelta
from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils                   import timezone
from django.http                    import HttpResponse
from .models                        import Order
from book.models                    import Book

@login_required
def order_list(request):
    # Только библиотекарь видит все заказы
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'order/order_list.html', {
        'orders': orders,
    })

@login_required
def my_orders(request):
    # Любой залогиненный пользователь видит только свои заказы
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order/my_orders.html', {
        'orders': orders,
    })

@login_required
def create_order(request):
    # Только гость (visitor, role=0) может создавать заказы
    if request.user.role != 0:
        return HttpResponse("Access denied", status=403)

    # дефолтная дата возврата через 30 дней
    default_due = (timezone.now() + timedelta(days=30)).date()

    if request.method == 'POST':
        book_id = request.POST.get('book')
        due_str = request.POST.get('due_date')  # ожидаем YYYY-MM-DD
        try:
            book = Book.objects.get(id=book_id)
            due  = timezone.datetime.fromisoformat(due_str)
            order = Order.create(user=request.user, book=book, plated_end_at=due)
            if order:
                return redirect('my_orders')
            else:
                error = "Cannot create order (maybe no copies or wrong date)"
        except Exception:
            error = "Invalid input"
        return render(request, 'order/create_order.html', {
            'books':      Book.objects.filter(count__gt=0),
            'default_due': default_due,
            'error':      error,
        })

    # GET: показываем форму создания заказа
    return render(request, 'order/create_order.html', {
        'books':       Book.objects.filter(count__gt=0),
        'default_due': default_due,
    })

@login_required
def close_order(request, order_id):
    # Только библиотекарь может закрыть (вернуть) заказ
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    order = get_object_or_404(Order, id=order_id)
    order.update(end_at=timezone.now())
    return redirect('order_list')

@login_required
def order_detail(request, order_id):
    # Детали конкретного заказа
    order = get_object_or_404(Order, id=order_id)

    # Доступ: библиотекарь видит все, пользователь — только свои
    if request.user.role == 1:
        can_close = (order.end_at is None)
    else:
        if order.user != request.user:
            return HttpResponse("Access denied", status=403)
        can_close = False

    return render(request, 'order/order_detail.html', {
        'order':     order,
        'can_close': can_close,
    })
