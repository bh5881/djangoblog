

from django import forms #首先继承Django的forms
from django.core.validators import RegexValidator  #导入正则校验器
from django_redis import get_redis_connection

from user.models import User

# 创建手机号码正则校验器
mobile_validator = RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式不正确！')


class CheckImageForm(forms.Form):
    """
    校验图形验证码
           1. 校验手机号码
        - 校验图形验证码
        - 校验是否在60s内有发送记录
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    mobile = forms.CharField(max_length=11, min_length=11, validators=[mobile_validator, ], error_messages={
        'max_length': '手机长度有误！',
        'min_length': '手机长度有误！',
        'required': '手机号码不能为空！'
    })

    captcha = forms.CharField(max_length=4, min_length=4, error_messages={
        'max_length': '图形验证码长度有误！',
        'min_length': '图形验证码长度有误！',
        'required': '图形验证码不能为空！'
    })

    def clean(self):
        clean_data = super().clean()
        mobile = clean_data.get('mobile')
        captcha = clean_data.get('captcha')
        # 如果前面的字段校验失败，mobile captcha 是 none
        # 如果前面的校验有问题，就不需要往下进行了
        if mobile and captcha:
            # 1.校验图形验证码
            # 获取session中保存的验证码，和 用户填入的进行比对
            image_code = self.request.session.get('image_code')
            if not image_code:
                raise forms.ValidationError('图形验证码失效')
            if image_code.upper() != captcha.upper():
                raise forms.ValidationError('图形验证码校验失败！')

            # 2.是否60秒以内发送过短信
            # 这个存在了 redis里面
            redis_conn = get_redis_connection(alias='verify_code')
            if redis_conn.get('sms_flag_{}'.format(mobile)):
                raise forms.ValidationError('获取短信验证码过于频繁！')

            # 3.校验手机号码是否注册
            if User.objects.filter(mobile=mobile).count():
                raise forms.ValidationError('手机号码已注册，请重新输入！')
        return clean_data


