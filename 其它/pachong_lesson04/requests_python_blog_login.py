import requests
login_url = 'http://182.61.29.114:1234/user/login/'
post={'account': 'admin',
'password': '123456',
'remember': 'false',}
headers = {'Cookie': 'csrftoken=BC7bh50wXYGNB2eTTg0vqdt0lfOCb2wxXuquNvjnE6oNFTHzxfnNbO0pSrpFt79y; sessionid=xw44nrubdkg92sttorrjra9mecuapaym',
'Host': '182.61.29.114:1234',
'Origin': 'http://182.61.29.114:1234',
'Referer': 'http://182.61.29.114:1234/user/login/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
'X-CSRFToken': 'BC7bh50wXYGNB2eTTg0vqdt0lfOCb2wxXuquNvjnE6oNFTHzxfnNbO0pSrpFt79y',
'X-Requested-With': 'XMLHttpRequest'}

response = requests.post(login_url,data=post,headers=headers)
# print(response.text)
# print(response.cookies)
#访问后台页面成功+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
first_url = 'http://182.61.29.114:1234/admin'
response2 = requests.get(first_url,headers=headers,cookies = response.cookies)
print(response2.text)

"""
返回了恭喜登录成功的字符：{"errno": "0", "errmsg": "\u606d\u559c\u767b\u5f55\u6210\u529f\uff01", "data": null}
<RequestsCookieJar[<Cookie csrftoken=HeSqrOCWDU5FZLMpsalReHaJ8tHn7oxh9c3B8c4lEtmLrAYWTh8zWSqKpSRAlld6 for 182.61.29.114/>, <Cookie sessionid=xw44nrubdkg92sttorrjra9mecuapaym for 182.61.29.114/>]


下一步则是携带cookie访问首页面，看是否出现admin的用户名
"""