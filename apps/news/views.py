import logging
from django.shortcuts import render
from django.views import View
from django.db.models import F
from django.core.paginator import Paginator
from .models import Tag, News, HotNews, Banner,Comments
from . import constants
from utils.res_code import json_response
from django.http import HttpResponseNotFound,JsonResponse
from utils.res_code import json_response, Code, error_map

logger = logging.getLogger('django')
# Create your views here.
"""
url地址：''
"""
def index(request):
    # 新闻标签
    hot_news = HotNews.objects.select_related('news').only('news__title','news__image_url','news_id').filter(is_delete=False).order_by('priority','-news__clicks')[:3]
    tags = Tag.objects.only('name').filter(is_delete=False)
    return render(request, 'news/index.html', context={
        'tags': tags,
        'hot_news':hot_news
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
        # return JsonResponse('589825485t')

class NewsDetailViews(View):
    """
    新闻详情视图
    url: /news/<int:news_id>
    """
    def get(self,request,news_id):
        # 校验是否存在
        news = News.objects.select_related('tag','author').only('title','update_time','tag__name','author__username').filter(is_delete=False,id = news_id).first()
        # news = News.objects.get(pk = news_id) #临时这样写前端可以查到

        # 获取评论
        comments = Comments.objects.select_related('author', 'parent__author').only('content', 'author__username',
                                                                                    'update_time',
                                                                                    'parent__author__username',
                                                                                    'parent__content',
                                                                                    'parent__update_time').filter(is_delete=False, news_id=news_id)

        # return render(request, 'news/news_detail.html', context={
        #     'news': news,
        #     'comments': comments
        # })
        if news:
            return render(request, 'news/news_detail_yuan.html', context={'news': news,'comments': comments})
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

class NewsCommentView(View):
    """
    添加评论视图
    url: /news/<int:news_id>/comment/
    """
    def post(self, request, news_id):
        # 是否登录
        if not request.user.is_authenticated:
            return json_response(errno=Code.SESSIONERR, errmsg=error_map[Code.SESSIONERR])

        # 新闻是否存在
        if not News.objects.filter(is_delete=False, id=news_id).exists():
            return json_response(errno=Code.PARAMERR, errmsg='新闻不存在！')

        # 判断内容
        content = request.POST.get('content')
        if not content:
            return json_response(errno=Code.PARAMERR, errmsg='评论内容不能为空')

        # 父id是否正常
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                parent_id = int(parent_id)
                if not Comments.objects.filter(is_delete=False, id=parent_id, news_id=news_id).exists():
                    return json_response(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
            except Exception as e:
                logger.info('前端传递过来的parent_id异常\n{}'.format(e))
                return json_response(errno=Code.PARAMERR, errmsg='未知异常')

        # 保存到数据库

        new_comment = Comments()
        new_comment.content = content
        new_comment.news_id = news_id
        new_comment.author = request.user
        if parent_id:
            new_comment.parent_id = parent_id
        # new_comment.parent_id = parent_id if parent_id else None
        new_comment.save()


        # 序列化一个评论数据

        return json_response(data=new_comment.to_dict_data())