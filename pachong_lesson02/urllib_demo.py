from urllib import request
import json

#使用代理的方式：
import  urllib3
Porxy = urllib3.ProxyManager('http://120.83.104.41:9999')
res = Porxy.request('get','http://httpbin.org/ip')
print(res.data)






#使用urllib3_______________________________________________
# import urllib3
# http = urllib3.PoolManager()
# response = http.request('get','http://httpbin.org/get')
# # print(response.data.decode('utf-8'))
# #变成字典的方法
# print(json.loads(response.data.decode('utf-8')))




#下载一张图片————————————————————————————————————————
# headers = {'user-agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
#            }
#
# req = request.Request(url='http://img95.699pic.com/photo/50008/9194.jpg_wh300.jpg',headers=headers)
#
# response = request.urlopen(req)
# # print(response.read())
# with open('test2.jpg','wb') as f:
#     f.write(response.read())
#————————————————————————————————
#使用request获取一张图片
# response = request.urlopen(url = 'http://httpbin.org/get')
# print(response.getcode())
# print(response.info())
# print(response.read())
