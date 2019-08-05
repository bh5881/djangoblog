from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'course'
"""
url地址：'course/'
"""
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.index,name = 'index'),
]