"""
此爬虫用面向对象的方法爬取全书网小说。
运用了requests 和beautifulsoup 和lxml 和etree 等库
"""

"""
存在问题：此处download中的session总是报错，也没有报错原因，后面打印返回值类型也是空值，并且在session.get（url）后面添加print也没有执行，总是直接跳转到后面的except
"""
import requests, logging, re
from bs4 import BeautifulSoup
from lxml import etree


class QuanShu:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'user-agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        })
        self.logger = logging.getLogger('quanshu')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        self.logger.addHandler(sh)

    def download(self, url):
        """
        下载器，传入小说章节url参数
        :param url:
        :return:
        """
        try:

            response = self.session.get(url)
            print('成功访问url')
            self.logger.info('成功访问 %s' % url)
            return response
        except Exception as e:
            self.logger.error('下载错误, url: %s' % url)

    def get_novel(self, novel_url):
        """
        根据小说的url现在整本小说，并保存到txt文件中
        :param novel_url:
        :return:
        """
        novel_title, novel_chapter_info = self.get_novel_info(novel_url)
        with open('%s.txt' % novel_title, 'w', encoding='utf-8') as f:
            f.write(novel_title)
            f.write('\n')
            for chapter_title, chapter_url in novel_chapter_info:
                f.write(chapter_title)
                f.write('\n')
                f.write(self.get_chapter_content(chapter_url))

    def get_novel_info(self, novel_url):
        """
        根据小说主页的url，返回小说的信息
        :param novel_url:
        :return: novel_title小说名，novel_chapter_info 列表，元素是二元数组
        """
        response = self.download(novel_url)
        if response:
            response.encoding = 'gbk'
            html = response.text
            novel_url, novel_chapter_info = self.parse_novel_info(html)
            return novel_url, novel_chapter_info
        else:
            self.logger.error('下载小说信息错误 url: %s' % novel_url)

    def get_chapter_content(self, chapter_url):
        """
        根据章节url返回小说内容
        :param chapter_url:
        :return:
        """
        response = self.download(chapter_url)
        if response:
            response.encoding = 'gbk'
            html = response.text
            chapter_content = self.pares_chapter_content(html)
            return chapter_content

    def parse_novel_info(self, html):
        """
        从html中解析出小说信息
        :param html:
        :return:
        """
        try:
            # 备用方案
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find_all('a', attrs={'class': 'article_title'})[0].string.strip()
            div = soup.find_all('div', attrs={'class': 'clearfix dirconone'})[0]
            lis = div.find_all('li')
            # 下面加最外层的大括号后变成生成器
            novel_chapter_info = [(li.a['title'], li.a['href']) for li in lis]
            print(title)
            print(len(lis))
            print(novel_chapter_info)
            print(len(novel_chapter_info))
            exit()
            # title = re.findall('class="article_title">(.*?)<',html)[0]
            # div = re.findall('<DIV class="clearfix dirconone">.*?</DIV>',html,re.S)[0]

            return title, novel_chapter_info
        except Exception as e:
            self.logger.error('解析小说信息失败')
            raise e

    def parse_chapter_content(self, html):
        try:
            page = etree.HTML(html)
            div = page.xpath('//div[@id = "content"]/text()')
            content = ''.join([x.strip() for x in div])
            return content
        except Exception as e:
            self.logger.error('解析章节失败')
            return '解析章节失败'


if __name__ == '__main__':
    spider = QuanShu()
    # spider.logger.error('aaaaa')
    # spider.get_novel('http://www.quanshuwang.com/book/138/138215')
    respons = spider.download('http://www.quanshuwang.com/book/138/138215')
    print(type(respons))
    respons.encoding = 'gbk'
    html = respons.text
    spider.parse_novel_info(html)
