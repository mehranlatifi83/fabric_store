# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UserRegistrationForm
from .models import Fabric, MyUser


def index(request):
    fabrics = Fabric.objects.all()
    return render(request, 'web/index.html', {"fabrics": fabrics})

# اضافه کردن تابع جستجو


def search(request):
    query = request.GET.get('query', '')
    # فرض بر این است که name فیلدی در مدل Fabric است
    results = Fabric.objects.filter(name__icontains=query)
    return render(request, 'web/search_results.html', {'fabrics': results, "search_text": query})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            user = MyUser.objects.filter(phone=phone).first()
            if user:
                # اگر شماره تلفن وجود داشته باشد، به فرم ورود با پسورد هدایت می‌شوند
                return redirect('password_login', phone=phone)
            else:
                # اگر شماره تلفن وجود نداشته باشد، به فرم ثبت‌نام هدایت می‌شوند
                return redirect('user_register', phone=phone)
    else:
        form = UserLoginForm()
    return render(request, 'web/login.html', {'form': form})


def password_login(request, phone):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # پیام خطا در صورت اشتباه بودن پسورد
            return render(request, 'web/password_login.html', {'error': 'پسورد اشتباه است', 'phone': phone})
    else:
        return render(request, 'web/password_login.html', {'phone': phone})


def user_register(request, phone):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=phone, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm(initial={'phone': phone})
    return render(request, 'web/register.html', {'form': form, "phone": phone})


def user_profile(request):
    return render(request, 'web/user_profile.html')

def admin_settings(request):
    users = MyUser.objects.all()
    fabrics = Fabric.objects.all()
    return render(request, 'web/admin_settings.html', {"users": users, "fabrics": fabrics})

def add_user(request):
    pass

def edit_user(request, user_id):
    pass

def delete_user(request, user_id):
    pass

def add_fabric(request):
    pass

def edit_fabric(request, fabric_id):
    pass

def delete_fabric(request, fabric_id):
    pass