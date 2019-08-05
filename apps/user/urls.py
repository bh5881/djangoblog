from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'user'
"""
url地址：'user/'
"""
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/',views.index,name = 'login'),
    path('register/',views.index2,name ='register')
]