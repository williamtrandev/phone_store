from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from applications.website.models import Customer, CartItem


def index(request):
    return render(request, 'pages/index.html')


def user_login(request):
    if 'customer' in request.session:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(username=username)

            if check_password(password, customer.password):
                customer_data = model_to_dict(customer)
                if 'password' in customer_data:
                    del customer_data['password']
                request.session['customer'] = customer_data
                cart_items_count = CartItem.objects.filter(customer=customer).aggregate(Sum('quantity'))['quantity__sum'] or 0
                request.session['cart_quantity'] = cart_items_count
                return redirect('index')
            else:
                return render(request, 'pages/login.html', {'error_message': 'Tài khoản hoặc mật khẩu không đúng'})

        except ObjectDoesNotExist:
            return render(request, 'pages/login.html', {'error_message': 'Tài khoản hoặc mật khẩu không đúng'})

    return render(request, 'pages/login.html')

def user_register(request):
    return render(request, 'pages/register.html')


def user_logout(request):
    if 'customer' in request.session:
        del request.session['customer']
    return redirect('login')
