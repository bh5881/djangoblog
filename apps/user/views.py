from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
"""
url地址：
"""
def index(request):
    return render(request, 'user/login.html')
    # return HttpResponse('zheshi')
def index2(request):
    return render(request, 'user/register.html')
    # return HttpResponse('zheshi')