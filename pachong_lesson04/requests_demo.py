import requests
response = requests.get('http://httpbin.org/get')
# response.encoding = 'utf-8' #如果显示乱码，可以用这个设置编码
# print(response)
# print(response.text) #获取文本

#测试post传参
info = {'username':'6566',
        'password':'999'}
# response2 = requests.post('http://httpbin.org/post',data=info)
# print(response2.text)

args = {
    'key1':'测试',
    'key2':'测试密码'
}
#自定义请求头
headers = {'aa':'bbb'}
#传入cookie
co = {'session_id':'123456'}
response5 = requests.get('http://www.quanshuwang.com')
response5.encoding = 'gbk'  #设置charset编码，如果没有声明charset就猜gbk或者utf-8
print(response5.text)



#下面是请求，上面写响应的方法++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#设置代理
# prox = {'http':'http://182.61.29.114:6868'}
# response4 = requests.get('http://httpbin.org/ip')
# print(response4.text)
#区别：data是form表单参数，params是url参数  可以自动对中文编码
# response3 = requests.post('http://httpbin.org/post',data=info,params=args,headers = headers,cookies = co)
# print(response3.request.url)
# print(response3.text)
# print(response3.request.headers['aa']) #可以拿到自定义请求头
# print(response3.cookies)




