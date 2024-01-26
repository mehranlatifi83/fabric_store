# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UserRegistrationForm, FabricForm
from .models import Fabric, MyUser
from django.contrib.auth.hashers import make_password

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
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # برای رمزگذاری پسورد قبل از ذخیره سازی
            form.instance.password = make_password(form.cleaned_data.get('password1'))
            form.save()
            return redirect('admin_settings')
    else:
        form = UserRegistrationForm()
    return render(request, 'web/add_edit_user.html', {'form': form})

def edit_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            # به‌روزرسانی پسورد اگر وارد شده باشد
            if form.cleaned_data.get('password1'):
                user.password = make_password(form.cleaned_data.get('password1'))
            user.save()
            return redirect('admin_settings')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'web/add_edit_user.html', {'form': form, 'user_object': user})

def delete_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_settings')
    return render(request, 'web/delete_confirm.html', {'user_object': user})

def add_fabric(request):
    if request.method == 'POST':
        form = FabricForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_settings')
    else:
        form = FabricForm()
    return render(request, 'web/add_edit_fabric.html', {'form': form})

def edit_fabric(request, fabric_id):
    fabric = get_object_or_404(Fabric, id=fabric_id)
    if request.method == 'POST':
        form = FabricForm(request.POST, request.FILES, instance=fabric)
        if form.is_valid():
            form.save()
            return redirect('admin_settings')
    else:
        form = FabricForm(instance=fabric)
    return render(request, 'web/add_edit_fabric.html', {'form': form, 'fabric': fabric})

def delete_fabric(request, fabric_id):
    fabric = get_object_or_404(Fabric, id=fabric_id)
    if request.method == 'POST':
        fabric.delete()
        return redirect('admin_settings')
    return render(request, 'web/delete_confirm.html', {'fabric': fabric})
