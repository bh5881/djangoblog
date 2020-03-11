"""
作业：用今天学的下载全书网的一个章节的小说内容，如果想搞得话，可以下载一本小说的内容
"""
from bs4 import BeautifulSoup
import requests
def get_chapter_content(chapter_url):

    # chapter_url = 'http://www.quanshuwang.com/book/44/44683/15380349.html'
    #获取响应内容，并编码成gbk格式
    response = requests.get(chapter_url)
    response.encoding = 'gbk'
    html = response.text
#创建解析对象
    soup =  BeautifulSoup(html, 'lxml')
    div = soup.find_all('div',attrs={'id':'content'})[0]
    #测试content内容
    # content = ''.join([x for x in div.strings][1:-1])
    #或者进行如下写法：
    content = []
    for item in div.strings:
        content.append(item)
    content = ''.join(content[1:-1])
    print(content)
    return content

def get_novel_info(novel_url):
    pass

def main(novel_url):
    """
    下载小说，主要逻辑
    :param novel_url:
    :return:
    """
get_chapter_content('http://www.quanshuwang.com/book/44/44683/15380349.html')