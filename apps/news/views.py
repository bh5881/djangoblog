import logging
from django.shortcuts import render
from django.views import View
from django.db.models import F
from django.core.paginator import Paginator
from .models import Tag, News, HotNews, Banner
from . import constants
from utils.res_code import json_response

logger = logging.getLogger('django')
# Create your views here.
"""
url地址：''
"""
def index(request):
    # 新闻标签
    tags = Tag.objects.only('name').filter(is_delete=False)
    return render(request, 'news/index.html', context={
        'tags': tags,
    })
    # return HttpResponse('zheshi')


class NewsListView(View):
    """
    新闻列表视图
    url : /news/
    args: tag, page
    """
    def get(self, request):
        # 1.获取参数
        try:
            tag_id = int(request.GET.get('tag', 0))
        except Exception as e:
            logger.error('标签错误：\n{}'.format(e))
            tag_id = 0

        try:
            page = int(request.GET.get('page', 0))
        except Exception as e:
            logger.error('页码错误：\n{}'.format(e))
            page = 1

        # 2.获取查询集 不会去数据库 惰性
        news_queryset = News.objects.values('id', 'title', 'digest', 'image_url', 'update_time').annotate(tag_name=F('tag__name'), author=F('author__username'))
        # 3.过滤
        # if tag_id:
        #     news = news_queryset.filter(is_delete=False, tag_id=tag_id)
        # else:
        #     news = news_queryset.filter(is_delete=False)

        news = news_queryset.filter(is_delete=False, tag_id=tag_id) or news_queryset.filter(is_delete=False)

        # 3.分页
        paginator = Paginator(news, constants.PER_PAGE_NEWS_COUNT)
        # 获取当前页数据 get_page 可以容错
        news_info = paginator.get_page(page)
        # 4.返回数据
        data = {
            'total_pages': paginator.num_pages,
            'news': list(news_info)
        }
        return json_response(data=data)


class NewsBannerView(View):
    """
    轮播图视图
    url: /news/banners/
    """
    def get(self, request):
        banners = Banner.objects.values('image_url', 'news_id').annotate(news_title=F('news__title')).filter(is_delete=False)[:constants.SHOW_BANNER_COUNT]

        data = {
            'banners': list(banners)
        }

        return json_response(data=data)