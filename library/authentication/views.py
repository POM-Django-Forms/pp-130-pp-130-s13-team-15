from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from authentication.models          import CustomUser
from order.models                   import Order

def home_view(request):
    return render(request, 'authentication/home.html')

def register_view(request):
    if request.method == 'POST':
        email      = request.POST.get('email')
        password   = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        role       = int(request.POST.get('role', 0))  # 0 — guest, 1 — librarian

        if email and password:
            user = CustomUser.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            if user:
                user.role      = role
                user.is_active = True
                user.save()
                return redirect('login')

    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user     = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'authentication/login.html', {
                'error': 'Invalid credentials'
            })
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# ----------------------------------------
# Список пользователей (только для библиотекаря)
# ----------------------------------------
@login_required
def user_list(request):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    users = CustomUser.objects.all()
    return render(request, 'authentication/user_list.html', {
        'users': users,
    })

# ----------------------------------------
# Детали пользователя + его заказы (только для библиотекаря)
# ----------------------------------------
@login_required
def user_detail(request, user_id):
    if request.user.role != 1:
        return HttpResponse("Access denied", status=403)

    user_obj = get_object_or_404(CustomUser, id=user_id)
    orders   = Order.objects.filter(user=user_obj).order_by('-created_at')

    return render(request, 'authentication/user_detail.html', {
        'user_obj': user_obj,
        'orders':   orders,
    })
