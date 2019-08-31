
from django.shortcuts import render
from django.http import HttpResponse , Http404
from django.views import View
from .models import Course
# Create your views here.
"""
url地址：
"""
class IndexView(View):
    """
    首页面
    url：/course/
    """
    def get(self,request):
        #拿到所有的视频数据
        courses = Course.objects.only('title','cover_url','teacher__name','teacher__title').select_related('teacher').filter(is_delete=False)
        #前端渲染
        return render(request,'course/course.html',context={'courses':courses})

class CourseDetailView(View):
    """
    课程详情视图：
    url： /course/<int:course_id>/
    """
    def get(self,request,course_id):
        #1，拿到课程细信息
        course= Course.objects.only('title','cover_url','video_url','profile','outline','teacher__name','teacher__photo','teacher__title').select_related('teacher').filter(is_delete=False,id = course_id)
        #渲染视图
        if course:
            course = course[0]
            return render(request,'course/course_detail.html',context={'course':course})
        else:
            return Http404('此课程不存在')
