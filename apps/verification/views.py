from django.shortcuts import render
import logging,random
from django.http import  HttpResponse,JsonResponse
from django.views import  View
from .forms import CheckImageForm
from django_redis import get_redis_connection
#内置库，系统库要放在最上面导入
#中间放Django库

from utils.res_code import json_response, Code, error_map
# Create your views here.
from util.captcha.captcha import captcha
from . import constants
from user.models import User
logger = logging.getLogger('django')
"""
url image_code/
1,生成一个验证码
2，在后端记录文本
3，生成一个日志
4，返回一个验证码

"""
def image_code_view(request):
    #生成一个验证码
    text,image = captcha.generate_captcha()
    #在后端记录文本
    request.session['image_code'] = text
    #给一个过期时间
    request.session.set_expiry(constants.IMAGE_CODE_EXPIRES)
    #3，生成一个日志
    logger.info('Image code:{}'.format(text))
    #4,返回验证码图片
    return HttpResponse(content=image,
                        content_type='image/jpg')
def check_username_view(request, username):
    """
校验username
urls: username/<username>(?P<username>\w{5,20})/
"""
    data = {
        "username": username,  # 查询用户名
        "count": User.objects.filter(username=username).count()  # 用户查询数量
            }
    return json_response(data = data)

def check_mobile_view(request, mobile):
    """
   校验手机号
   urls： mobile/<mobile>(?P<mobile>1[0-9]\d{9})/
   """
    data = {
        "mobile": mobile,  # 查询用户名
        "count": User.objects.filter(mobile=mobile).count()  # 用户查询数量
            }
    # return JsonResponse(data)
    return json_response(data = data)

class SmsCodeView(View):
    def post(self,request):
        # 1,校验手机号码
        # mobile = request.POST.get('mobile')
        print('开始执行view')
        form = CheckImageForm(request.POST,request=request)
        if form.is_valid():
            #获取手机号码
            mobile = form.cleaned_data.get('mobile')
            #生成短信验证码
            sms_code = ''.join([random.choice('0123456789')for i in range(constants.SMS_CODE_LENGTH)])
            #发送短信验证码 调用接口
            print('333')
            logger.info('发送短信验证码[正常][mobile:%s sms_code: %s]'%(mobile,sms_code))
            #保存这个验证码，时限redis
            #创建短信验证码发送记录
            sms_flag_key = 'sms_flag_{}'.format(mobile)
            #创建短信验证码内容的key
            sms_text_key = 'sms_text_{}'.format(mobile)
            redis_conn = get_redis_connection(alias='verify_code')
            pl = redis_conn.pipeline()
            try:
                pl.setex(sms_flag_key,constants.SMS_CODE_INTERVAL,1)
                pl.setex(sms_text_key,constants.SMS_CODE_EXPIRES*60,sms_code)
                #让管道通知redis执行命令
                pl.execute()
                print('zhixingwanbi')
                return json_response(errmsg='短信验证码发送成功')
            except Exception as e:
                logger.error('redis 执行异常：{}'.format(e))
                return json_response(errno=Code.UNKOWNERR,errmsg=error_map[Code.UNKOWNERR])
        else:
            err_msg_list= []
            for item in form.errors.values(): #此处item是一个列表#有时间调试一下看错误的值里面有什么
                err_msg_list.append(item[0])
                err_msg_str = '/'.join(err_msg_list)
                # return json_response(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])
                return json_response(errno=Code.PARAMERR, errmsg=err_msg_str)


        # 2,校验图形验证码

    def get(self,request):
        pass