from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import JsonResponse

from applications.website.models import Staff

def index(request):
    return render(request, 'pages/index.html')


def user_login(request):
    if 'username' in request.session:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            staff = Staff.objects.get(username=username)

            if check_password(password, staff.password):
                staff_data = model_to_dict(staff)
                if 'password' in staff_data:
                    del staff_data['password']
                request.session['staff'] = staff_data
                return redirect('index')
            else:
                return render(request, 'pages/login.html', {'error_message': 'Username or password is incorrect'})

        except ObjectDoesNotExist:
            return render(request, 'pages/login.html', {'error_message': 'Username or password is incorrect'})

    return render(request, 'pages/login.html')

def user_register(request):
    return render(request, 'pages/register.html')


def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'user_type' in request.session:
        del request.session['user_type']
    return redirect('login')
