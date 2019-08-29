from PIL import Image

from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.views import View
from django.core.paginator import Paginator
from django.http import FileResponse, Http404

from .models import Doc
from . import constants
from utils.res_code import json_response
"""
url: doc/
path('download/', views.index, name='index'),
    path('docs/', views.DocListView.as_view(), name='doc_list'),
"""

def index(request):

    return render(request, 'doc/docDownload.html')


class DocListView(View):
    def get(self, request):
        # 1. 拿到所有文档
        docs = Doc.objects.values('file_url', 'file_name', 'title', 'desc', 'image_url').filter(is_delete=False)
        # 2. 分页
        paginator = Paginator(docs, constants.PER_PAGE_DOC_COUNT)

        try:
            page = paginator.get_page(int(request.GET.get('page')))
        except Exception as e:
            page = paginator.get_page(1)

        # 3. 序列化
        data = {
            'total_page': paginator.num_pages,
            'docs': list(page)
        }
        # 4. 返回json响应
        return json_response(data=data)


class DownLoadView(View):
    """
    下载视图
    """
    def get(self, request, *args, **kwargs):
        # 复杂的逻辑生成一个文件流（内存中）
        f = open('/home/pyvip/mysite48/media/django项目班_英语单词.jpg', 'rb')

        # 创建一个响应
        try:
            res = FileResponse(f)
        except Exception as e:
            raise Http404('文档下载异常')

        ex_name = 'xls'                 # 获取文件后缀

        if not ex_name:
            raise Http404("文档url异常！")
        else:
            ex_name = ex_name.lower()

        if ex_name == "pdf":
            res["Content-type"] = "application/pdf"
        elif ex_name == "zip":
            res["Content-type"] = "application/zip"
        elif ex_name == "doc":
            res["Content-type"] = "application/msword"
        elif ex_name == "xls":
            res["Content-type"] = "application/vnd.ms-excel"
        elif ex_name == "docx":
            res["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif ex_name == "ppt":
            res["Content-type"] = "application/vnd.ms-powerpoint"
        elif ex_name == "pptx":
            res["Content-type"] = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

        else:
            raise Http404("文档格式不正确！")

        doc_filename = escape_uri_path('某某.jpg')

        res['Content-Disposition'] = "attachment; filename*=UTF-8''{}".format(doc_filename)
        return res