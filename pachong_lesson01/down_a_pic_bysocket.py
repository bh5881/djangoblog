"""
使用爬虫下载一张图片，socket底层技术
"""
import socket
import re
#创建一个socket
client = socket.socket()
#获取图片的url
img_url = 'http://seopic.699pic.com/photo/50055/5642.jpg_wh1200.jpg'
img_url2 = 'http://182.61.29.114:1234/media/jichujiaochen.jpeg'
#构造请求报文
data = 'GET /photo/50055/5642.jpg_wh1200.jpg HTTP/1.1\r\nHost: seopic.699pic.com\r\n\r\n'
#连接服务端
client.connect(('seopic.699pic.com',80))
#发送请求   注意二进制
client.send(data.encode())
#接收响应
img_data = b''
#接收第一次请求的数据： 此处可以写4096但是Windows一次只能接收1024
first_data = client.recv(1024)
#获取响应数据的长度
length = int(re.findall(b'Content-Length: (.*?)\r\n',first_data)[0])
print(length)
print(first_data)
#获取第一次请求里的图片数据，根据\r\n\r\n
#因为是不可见字符，所以加re.S
img_data += re.findall(b'\r\n\r\n(.*)',first_data,re.S)[0]
#获取剩余的数据
while True:
    temp = client.recv(1024)
    if temp:
        img_data += temp
        if len(img_data) >= length: #s数据接收完成
            break
    else:
        break
#测试比较文件长度
print(len(img_data) ,length)
with open('test.jpg','wb') as f:
    f.write(img_data)



"""
作业：重复上面的代码，使用爬虫下载一张图片
"""


# while True:
#     res = client.recv(1024)
#     if res:
#         print(res)
#     else:
#         break

"""
测试成功，拿到数据，二进制
"""

