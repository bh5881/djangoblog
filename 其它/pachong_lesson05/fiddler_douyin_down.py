import requests
url = 'http://v3-dy-z.ixigua.com/a3419b52d31782d84ca4b35d5fb83f9e/5d8273b1/video/m/22038d84f1c26374dadb5ad3abcf3ce42341162e9ed500005f9f1a87589c/?a=1128&br=1124&cr=3&cs=2&dr=0&ds=1&er=&l=20190919011258010008058215412535&lr=&rc=ajk0ams4MzxlcDMzNmkzM0ApZDhmZjczOjs0NzU8NjdlOmdhcWNsNC5hMi1fLS1eLTBzczRiYTE1LzQxNDYyXmJjMTE6Yw%3D%3D'
headers  = {
'User-Agent': 'ttplayer(2.9.5.353)',
'Accept': '*/*',
'Icy-MetaData':'1',
'Accept-Encoding': 'identity',
'Host': 'v3-dy-z.ixigua.com',
'Connection': 'Keep-Alive',

}
response = requests.get(url , headers= headers)

with open('doyin.mp4','wb') as f:
    f.write(response.content)
