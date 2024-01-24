# views.py
from django.shortcuts import render
from .models import Fabric  # فرض بر این است که مدل Fabric را ایجاد کرده‌اید

def index(request):
    fabrics = Fabric.objects.all()
    return render(request, 'web/index.html', {"fabrics": fabrics})

# اضافه کردن تابع جستجو
def search(request):
    query = request.GET.get('query', '')
    results = Fabric.objects.filter(name__icontains=query)  # فرض بر این است که name فیلدی در مدل Fabric است
    return render(request, 'web/search_results.html', {'fabrics': results, "search_text" : query})
