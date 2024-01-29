# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import UserLoginForm, UserRegistrationForm, FabricForm, AddressForm, EmailChangeForm, CustomPasswordChangeForm
from .models import Fabric, MyUser, State, City, Address, EmailActivation
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
import os
from django.conf import settings
from django.db.models import Q

def index(request):
    fabrics = Fabric.objects.all()
    return render(request, 'web/index.html', {"fabrics": fabrics})

# اضافه کردن تابع جستجو


def search(request):
    query = request.GET.get('query', '')
    # فرض بر این است که name فیلدی در مدل Fabric است
    results = Fabric.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query) | Q(price__icontains=query))
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
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, 'web/user_profile.html', {"user_addresses": user_addresses})

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

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('user_profile')
    else:
        form = AddressForm()
    return render(request, 'web/add_edit_address_for_user.html', {'form': form})

def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'web/add_edit_address_for_user.html', {'form': form, 'address': address})

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        address.delete()
        return redirect('user_profile')
    return render(request, 'web/delete_confirm.html', {'address': address})

def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return JsonResponse({"cities": list(cities.values('id', 'name'))})

def load_states_and_cities(request):
    if request.user.is_authenticated and request.user.is_admin:
        # مسیر فایل JSON
        file_path = os.path.join(settings.BASE_DIR, 'web', 'data', 'provinces-any-cities.json')

        # خواندن فایل JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # ایجاد استان‌ها و شهرها در پایگاه داده
            for state_data in data:
                state, created = State.objects.get_or_create(name=state_data['name'])
                for city_data in state_data['cities']:
                    City.objects.get_or_create(name=city_data['name'], state=state)
        return render(request, 'web/load_states_cities.html')
    else:
        return HttpResponse("شما اجازه دسترسی به این قسمت رو ندارین")

def send_activation_email(email, activation_key):
    activation_url = f"{settings.SITE_URL}{reverse('email_activate', kwargs={'activation_key': activation_key})}"
    message = f"برای فعالسازی ایمیل خود بر روی لینک زیر کلیک کنید\n{activation_url}\nبا تشکر. پارچه سرای محمد"
    html_message = f'برای فعال‌سازی ایمیل خود <a href="{activation_url}">اینجا</a> کلیک کنید\nبا تشکر. پارچه سرای محمد'
    send_mail(subject='فعال‌سازی ایمیل', message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email], html_message=html_message)

def change_email_request(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            if request.user.email == new_email:
                return render(request, "web/user_profile.html", {"message": "ایمیل وارد شده با ایمیل فعلی شما یکسان است."})
            activation_record = EmailActivation.objects.create(user=request.user, email=new_email)
            send_activation_email(new_email, activation_record.activation_key)
            return render(request, "web/user_profile.html", {"message": "لینک فعال‌سازی به ایمیل شما ارسال شد."})
def activate_email(request, activation_key):
    try:
        activation_record = EmailActivation.objects.get(activation_key=activation_key, is_activated=False)
        user = activation_record.user
        user.email = activation_record.email
        user.save()
        activation_record.is_activated = True
        activation_record.save()
        send_mail(subject="فعالسازی ایمیل", message="ایمیل شما با موفقیت تغییر یافت\nبا تشکر. پارچه سرای محمد", from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email], html_message=f'ایمیل شما با موفقیت تغییر یافت. برای ورود به سایت <a href="{settings.SITE_URL} کلیک نمایید\nبا تشکر پارچه سرای محمد"')
        return render(request, "web/user_profile.html", {"message": "ایمیل شما با موفقیت تغییر یافت."})
    except EmailActivation.DoesNotExist:
        return render(request, "web/user_profile.html", {"message": "درخواست نامعتبر است."})

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            update_session_auth_hash(request, user)  # به روز رسانی session برای جلوگیری از خروج کاربر
            return render(request, "web/user_profile.html", {"message": "رمز عبور شما با موفقیت تغییر کرد"})
        else:
            message = "خطایی در تغییر رمز عبور پیش آمد. لطفا دوباره امتحان کنید"
            return render(request, "web/user_profile.html", {"message": message})