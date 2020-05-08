#测试socket服务 基础
import socket
#创建一个socket服务端
server = socket.socket()
#绑定ip和端口
server.bind(('0.0.0.0',8000))
#监听
server.listen(5)
while True:
    conn , addr = server.accept()
    #接收数据
    data = conn.recv(1024)
    print(data)
    #发送数据
    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n\r\n这是一个服务器测试的'.encode())
    conn.close()
"""
接收结果：
b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\r\nSec-Fetch-Site: none\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9\r\nCookie: csrftoken=V0ouoqHNBcFUAUZSunOTdHdMXNGyRHbWnW4RehurzVZcVgG5eIqBaBqZ2sNFnBdT\r\nDNT: 1\r\n\r\n'
"""