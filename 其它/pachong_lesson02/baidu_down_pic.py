"""
作业二：下载百度图片首页的所有图片

"""
import urllib3
import re
import json
page_url = 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%B7%E7%BE%B0&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111'

#下载html
http = urllib3.PoolManager()
res = http.request('get',page_url)
#此处搜索charset来找到网页的编码格式
# html = res.data.decode('utf-8')
# #通过正则获取所有的下载图片地址
# img_urls = re.findall(r'"thumbURL":"(.*?)"',html)
# print(img_urls)
#构造请求头，防止防盗链检查
# headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
#     'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%B7%E7%BE%B0&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111'
# }
headers = {'user-agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',}
#遍历下载
# for index , img_url in enumerate(img_urls):
#     #添加请求头
#     print(img_url)
#     img_res = http.request('get',img_url)
#     #动态拼接文件名
#     img_file_name = '%s.%s'%(index,img_url.split('.')[-1])
#     with open(img_file_name,'wb') as f:
#         #此处要使用.data来获取数据
#         f.write(img_res.data)

#百度图片ajax下载——————————————————————————————————————————————————
url_ajax = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%A3%8E%E6%99%AF&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word=%E9%A3%8E%E6%99%AF&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&pn={}&rn=30&gsm=&1568724543636='
for i in range(1,4):
    url = url_ajax.format(i*30)
    res=http.request('get',url)
    #json格式的字符一定是utf-8的编码格式
    data  = json.loads(res.data.decode('utf-8'))
    #下面请求的包含搜索的关键词信息，若需要数据，只需将字典中的data键值提取出来
    # print(data)
    # print(data['data'])
    #暂时只打印一次的方法，用exit（）退出
    # img_info_list = data['data']
    img_info_list = res.data.decode('utf-8')
    print(type(img_info_list))
    # print(img_info_list)
    img_urls =  re.findall(r'"thumbURL":"(.*?)"',img_info_list)
    print(img_urls)
    #开始下载图片：
    for index, img_url in enumerate(img_urls):
    # #添加请求头
        print(img_url)
        img_res = http.request('get',img_url,headers=headers)
    #     #动态拼接文件名
        try:
            img_file_name = '%s.%s'%(index,img_url.split('.')[-1])
            with open(str(i)+'页'+str(index)+'张'+img_file_name,'wb') as f:
                #此处要使用.data来获取数据
                f.write(img_res.data)
        except:
            print('下载失败'+str(i)+'页'+str(index)+'张')


    # for img in img_info_list:
    #     # print(img['thumbURL'])
    #     # print(img)
    #     img_urls = re.findall("thumbURL': '(.*?)",img)
    #     print(img_urls)



