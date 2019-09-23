import requests
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
post={
'ck': '',
'name': '2446867994@qq.com',
'password': 'python110',
'remember': 'false',
'ticket': '',
}
headers={
'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
response = requests.post(login_url,data=post,headers =headers )
# print(response.text)
url2 = 'https://www.douban.com'
response2 = requests.get(url2,cookies = response.cookies,headers= headers)
print(response2.text)
"""
测试成功，结果在打印结果中发现“<span>hahahahaha的帐号</span><span class="arrow"></span>”
"""