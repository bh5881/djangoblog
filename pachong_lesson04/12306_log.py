
"""
流程：
登录首页，获取cookies
访问图像验证码，获取图像验证码
输入图像验证码位置参数
传递位置参数和其他的附加信息以get的方式传递给校验url
最后获取返回的校验结果


最后优化代码，用session保持会话的技术。有待以后了解

"""





#优化代码：
import requests
import re
import base64
login_page_url = 'https://kyfw.12306.cn/otn/resources/login.html'
#访问首页面
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
session = requests.Session()
#添加ua
session.headers.update(headers)

cookies = None
response = session.get(login_page_url )
#下载img图片验证码
captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1568810291213&callback=jQuery1910002608780921482534_1568809853704&_=1568809853705'
captcha_response = session.get(captcha_url )

# print(captcha_response.text)
# print(captcha_response.content)
img_data = re.findall(b'"image":"(.*?)"',captcha_response.content)[0]
res_img = base64.b64decode(img_data)
# print(img_data)
def get_point_by_index(index):
    map = {
        '1':'39,43',
        '2':'109,43',
        '3':'185,43',
        '4':'253,43',
        '5':'39,121',
        '6':'109,121',
        '7':'185,121',
        '8':'253,121',
    }
    index = index.split(',')
    temp = []
    for index in index:
        temp.append(map[index])
        return ','.join(temp)
with open('capcha.jpg','wb')as f:
    f.write(res_img)
captcha_check_api = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
args = {
'callback': 'jQuery1910002608780921482534_1568809853704',
'answer': get_point_by_index(input('请输入图形验证码')),
'rand': 'sjrand',
'login_site': 'E',
'_': '1568809853706',
}

#验证用
# print(args)

check_response = session.get(captcha_check_api,params=args  )
print(check_response.text)













# import requests
# import re
# import base64
# login_page_url = 'https://kyfw.12306.cn/otn/resources/login.html'
# #访问首页面
# headers={
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
# }
# cookies = None
# response = requests.get(login_page_url,headers=headers)
# cookies = response.cookies
# #下载img图片验证码
# captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1568810291213&callback=jQuery1910002608780921482534_1568809853704&_=1568809853705'
# captcha_response = requests.get(captcha_url,headers = headers, cookies=cookies)
# cookies= captcha_response.cookies
# # print(captcha_response.text)
# # print(captcha_response.content)
# img_data = re.findall(b'"image":"(.*?)"',captcha_response.content)[0]
# res_img = base64.b64decode(img_data)
# # print(img_data)
# def get_point_by_index(index):
#     map = {
#         '1':'39,43',
#         '2':'109,43',
#         '3':'185,43',
#         '4':'253,43',
#         '5':'39,121',
#         '6':'109,121',
#         '7':'185,121',
#         '8':'253,121',
#     }
#     index = index.split(',')
#     temp = []
#     for index in index:
#         temp.append(map[index])
#         return ','.join(temp)
# with open('capcha.jpg','wb')as f:
#     f.write(res_img)
# captcha_check_api = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
# args = {
# 'callback': 'jQuery1910002608780921482534_1568809853704',
# 'answer': get_point_by_index(input('请输入图形验证码')),
# 'rand': 'sjrand',
# 'login_site': 'E',
# '_': '1568809853706',
# }
#
# #验证用
# # print(args)
#
# check_response = requests.get(captcha_check_api,params=args,headers=headers,cookies = cookies)
# print(check_response.text)