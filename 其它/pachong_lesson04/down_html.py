import re, requests,os
url = 'http://www.quanshuwang.com'
response = requests.get(url)
response.encoding = 'gbk'
content = response.text
# print(content)
headers={
'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
#获取静态文件，js和图片格式的文件，返回一个集合
def static(content):
    tils = re.findall(r'src="(.*?)"',content)
    # print(tils_set)
    return tils
#获取css静态文件，返回一个集合
def css(content):
    csss = re.findall(r'href="(.*?)"',content)
    clean_css = []
    for i in csss:
        if i.endswith('css'):
            clean_css.append(i)
    return clean_css
    # print(clean_css)
# css(content)
def title(content):
    return re.findall(r'<title>(.*?)</title>',content)[0]
# print(title(content))

def down_static(url_list):
    for i in url_list:
        if i.startswith('http'):
            if os.path.exists(title(content)):
                # print(title(content))
                filename = title(content)+'/'+i.split('/')[-1]
                if i.endswith('js'):
                    with open(filename, 'w') as f:
                        f.write(requests.get(i, headers=headers).text)
                else:
                    with open(filename, 'wb') as f:
                        f.write(requests.get(i, headers=headers).content)
            else:
                os.mkdir(title(content))
                # print('ceshi')
                filename = title(content) + '/'+i.split('/')[-1]

                if i.endswith('js'):
                    with open(filename, 'w') as f:
                        f.write(requests.get(i, headers=headers).text)
                else:
                    with open(filename, 'wb') as f:
                        f.write(requests.get(i, headers=headers).content)

        else:
            down_url = url + i
            if os.path.exists(title(content)):
                # print(title(content))
                filename = title(content)+'/'+i.split('/')[-1]
                with open(filename,'w') as f:
                    f.write(requests.get(down_url,headers=headers).text)
            else:
                os.mkdir(title(content))
                # print('ceshi')
                filename = title(content) + '/'+i.split('/')[-1]
                with open(filename, 'w') as f:
                    f.write(requests.get(down_url,headers=headers).text)


down_static(css(content))
down_static(static(content))
#定义新的content：
def new_content(content):
    for i in css(content):
        new_addr = './'+title(content) +'/'+ i.split('/')[-1]
        content = content.replace(i,new_addr)
        print(new_addr)
    for a in static(content):
        new_addr = './'+title(content) +'/'+ a.split('/')[-1]
        content = content.replace(a,new_addr)
        print(new_addr)
    return content

# new_content(content)
with open(title(content)+'.html','w',encoding='gbk') as f:
    f.write(new_content(content))
    print('下载成功')





