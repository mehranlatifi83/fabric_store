# urls.py
from django.urls import path
from .views import index, search, user_login, password_login, user_register, user_profile, admin_settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),  # URL جستجو
    path('login/', user_login, name='user_login'),
    path('profile/', user_profile, name='user_profile'),
    path('login/password/<str:phone>/', password_login, name='password_login'),
    path('register/<str:phone>/', user_register, name='user_register'),
    path("setting/", admin_settings, name="admin_settings"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
