from django import forms
from django_redis import get_redis_connection
import re
from django.db.models import Q
from verification import constants
from .models import User
from django.contrib.auth import login
from verification.forms import mobile_validator

#用户注册
class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    username = forms.CharField(label='用户名', max_length=20, min_length=5, error_messages={
        'max_length': '用户名长度要小于20',
        'min_length': '用户名长度要大于5',
        'required': '用户名不能为空',
    })
    password = forms.CharField(label='密码', max_length=20, min_length=6, error_messages={
        'max_length': '密码长度要小于20',
        'min_length': '密码长度要大于5',
        'required': '密码不能为空',
    })
    password_repeat = forms.CharField(label='确认密码', max_length=20, min_length=6, error_messages={
        'max_length': '密码长度要小于20',
        'min_length': '密码长度要大于5',
        'required': '密码不能为空',
    })
    mobile = forms.CharField(label='手机号码', max_length=11, min_length=11, validators=[mobile_validator, ], error_messages={
        'max_length': '手机号码长度不正确',
        'min_length': '手机号码长度不正确',
        'required': '手机号码不能为空',
    })
    sms_code = forms.CharField(label='短信验证码', max_length=constants.SMS_CODE_LENGTH, min_length=constants.SMS_CODE_LENGTH, error_messages={
        'max_length': '短信验证码长度不正确',
        'min_length': '短信验证码长度不正确',
        'required': '短信验证码不能为空',
    })

    def clean_username(self):
        """
        校验用户名
        :return:
        """
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')

        return username

    def clean_mobile(self):
        """
        校验手机号码
        :return:
        """
        mobile = self.cleaned_data.get('mobile')

        if User.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('手机号码已注册！')

        return mobile

    def clean(self):
        """
        联合校验
        :return:
        """
        clean_data = super().clean()
        # 校验密码是否一致
        password = clean_data.get('password')
        password_repeat = clean_data.get('password_repeat')

        if password != password_repeat:
            raise forms.ValidationError('两次密码不一致！')

        # 校验短信验证码
        sms_code = clean_data.get('sms_code')
        moblie = clean_data.get('mobile')

        redis_conn = get_redis_connection(alias='verify_code')
        real_code = redis_conn.get('sms_text_{}'.format(moblie))
        if (not real_code) or (real_code.decode('utf-8') != sms_code):
            raise forms.ValidationError('短信验证码错误!')


class LoginForm(forms.Form):
    account = forms.CharField(error_messages={'required': '账户不能为空'})

    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={
                                   'max_length': '密码长度要小于20',
                                   'min_length': '密码长度要大于6',
                                   'require': '密码不能为空'
                               })
    remember = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)#添加request
        super().__init__(*args, **kwargs)

    def clean_account(self):
        """
        校验用户名
        :return:
        """
        account = self.cleaned_data.get('account')

        if not re.match(r'^1[3-9]\d{9}$', account) and (len(account) < 5 or len(account) > 20):
            raise forms.ValidationError('用户账户格式不正确，请重新输入')

        # if re.match(r'^1[3-9]\d{9}$', account):
        #     pass
        # else:
        #     if len(account) < 5 or len(account) > 20:
        #         raise forms.ValidationError('用户账户格式不正确，请重新输入')

        return account

    def clean(self):
        """
        校验用户名密码， 并实现登录逻辑
        :return:
        """
        # cleaned_data = super().clean()

        account = self.cleaned_data.get('account')
        password = self.cleaned_data.get('password')
        remember = self.cleaned_data.get('remember')

        # 登录逻辑
        # 判断用户名密码是否匹配
        # 1.先找到这个用户
        # select * from tb_user where mobile=account or username=account;
        #前面需要导入from django.db.models import Q
        user_queryset = User.objects.filter(Q(mobile=account)|Q(username=account))
        # 判断用户是否存在
        if user_queryset:
            # 2.校验这个密码是否匹配
            user = user_queryset.first()
            if user.check_password(password):
                # 是否免登录
                if remember:
                    # 免登录14天
                    self.request.session.set_expiry(14*24*60*60)
                else:
                    # 关闭浏览器清除登录状态
                    self.request.session.set_expiry(0)
                # 登录
                #需要导入from django.contrib.auth import login
                login(self.request, user)
            else:
                raise forms.ValidationError('用户名密码错误！')
        else:
            raise forms.ValidationError('用户账户不存在，请重新输入！')

        return self.cleaned_data