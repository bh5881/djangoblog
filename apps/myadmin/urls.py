# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝 2019/8/27 20:49

from django.urls import path

from . import views

app_name = 'myadmin'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('wait/', views.WaitView.as_view(), name='wait'),
    path('menus/', views.MenuListView.as_view(), name='menu_list'),
    path('menu/', views.MenuAddView.as_view(), name='menu_add'),
    path('menu/<int:menu_id>/', views.MenuUpdateView.as_view(), name='menu_update'),
    path('users/',views.UserListView.as_view(),name = 'user_list'),
path('user/<int:user_id>/', views.UserUpdateView.as_view(), name='user_update'),
]
