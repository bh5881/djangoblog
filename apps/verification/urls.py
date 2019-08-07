
from django.urls import path
from . import views

app_name = 'verification'
urlpatterns = [
    path('image_code/',views.image_code_view,name = 'image_code')
]