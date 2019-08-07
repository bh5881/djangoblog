from django.shortcuts import render
import logging
from django.http import  HttpResponse
#内置库，系统库要放在最上面导入
#中间放Django库

# Create your views here.
from util.captcha.captcha import captcha
from . import constants
logger = logging.getLogger('django')
"""
url image_code/
1,生成一个验证码
2，在后端记录文本
3，生成一个日志
4，返回一个验证码

"""
def image_code_view(requeset):
    #生成一个验证码
    text,image = captcha.generate_captcha()
    #在后端记录文本
    requeset.session['image_code'] = text
    #给一个过期时间
    requeset.session.set_expiry(constants.IMAGE_CODE_EXPIRES)
    #3，生成一个日志
    logger.info('Image code:{}'.format(text))
    #4,返回验证码图片
    return HttpResponse(content=image,
                        content_type='image/jpg')
