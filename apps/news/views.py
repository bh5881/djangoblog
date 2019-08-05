from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
"""
url地址：
"""
def index(request):
    return render(request, 'news/index.html')
    # return HttpResponse('zheshi')