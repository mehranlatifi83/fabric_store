# urls.py
from django.urls import path
from .views import index, search  # فرض بر این است که تابع search را اضافه کرده‌اید

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),  # URL جستجو
]
