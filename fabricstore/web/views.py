from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>سلام</h1>\nبه صفحه اصلی سایت خوش اومدین.")