from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'news'
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.index),
]