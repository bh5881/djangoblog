from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'user'
"""
url地址：'user/'
"""
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/',views.RegisterView.as_view(),name ='register'),
    path('logout/',views.LogoutView.as_view(),name = 'logout'),
# path('logout/', views.LogoutView.as_view(), name='logout')

]