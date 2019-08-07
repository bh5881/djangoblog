from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
"""
url地址：doc/
"""
def index(request):
    return render(request, 'doc/docDownload.html')
    # return HttpResponse('zheshi')