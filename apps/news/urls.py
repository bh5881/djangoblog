from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'news'
"""
url地址：''
"""
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.index,name = 'index'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/banners/',views.NewsBannerView.as_view(),name = 'news_banner'),
    path('news/<int:news_id>/',views.NewsDetailViews.as_view(),name = 'news_detail'),
path('news/<int:news_id>/comment/', views.NewsCommentView.as_view(), name='news_comment'),
    path('news/search/',views.NewsSearchViews.as_view(),name = 'news_search'),
    # path('test/',views.addtemp),

]