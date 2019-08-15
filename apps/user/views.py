from django.shortcuts import render
from django.http import HttpResponse
from utils.res_code import json_response ,Code
from django import forms
from .models import User
from django.views import View
from .forms import RegisterForm ,LoginForm
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

class LoginView(View):
    """
    登录视图
    url： /user/login/
    """
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 1.先校验
        #此处添加request=request是为了在form里可以校验session以便添加几天免登陆
        form = LoginForm(request.POST, request=request)#此处loginForm在form里已经被复写加了request
        if form.is_valid():#传入request后就能用session了

            return json_response(errmsg='恭喜登录成功！')
        else:
            # 将表单的报错信息进行拼接
            err_msg_list = []
            for item in form.errors.values():
                err_msg_list.append(item[0])

            err_msg_str = '/'.join(err_msg_list)
            return json_response(errno=Code.PARAMERR, errmsg=err_msg_str)

class RegisterView(View):
    """
    注册视图
    url: '/user/register/'
    """
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        # 1. 校验数据
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 2. 创建数据
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mobile = form.cleaned_data.get('mobile')
            User.objects.create_user(username=username, password=password, mobile=mobile)
            return json_response(errmsg='恭喜您，注册成功！')
        else:
            # 将表单的报错信息进行拼接
            err_msg_list = []
            for item in form.errors.values():
                err_msg_list.append(item[0])

            err_msg_str = '/'.join(err_msg_list)
            return json_response(errno=Code.PARAMERR, errmsg=err_msg_str)