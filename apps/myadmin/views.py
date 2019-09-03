from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Menu
from .forms import MenuModelForm
from utils.res_code import json_response, Code


class IndexView(View):
    def get(self, request):
        # 通过用户，通过权限，去获取这个列表
        menus = [
            {
                "name": "工作台",
                "url": "myadmin:home",
                "icon": "fa-desktop"
            },
            {
                "name": "新闻管理",
                "icon": "fa-newspaper-o",
                "children": [
                    {
                        "name": "新闻标签管理",
                        "url": "myadmin:wait"
                    }, {
                        "name": "新闻管理",
                        "url": "myadmin:wait"
                    }, {
                        "name": "热门新闻管理",
                        "url": "myadmin:wait"
                    }
                ]
            },
            {
                "name": "轮播图管理",
                "icon": "fa-picture-o",
                "url": "myadmin:wait"
            },
            {
                "name": "文档管理",
                "icon": "fa-folder",
                "url": "myadmin:home"
            },
            {
                "name": "在线课堂",
                "icon": "fa-book",
                "children": [
                    {
                        "name": "课程分类管理",
                        "url": "myadmin:wait"
                    },
                    {
                        "name": "课程管理",
                        "url": "myadmin:wait"
                    },
                    {
                        "name": "讲师管理",
                        "url": "myadmin:wait"
                    }
                ]
            },
            {
                "name": "系统设置",
                "icon": "fa-cogs",
                "children": [
                    {
                        "name": "权限管理",
                        "url": "myadmin:wait"
                    },
                    {
                        "name": "用户管理",
                        "url": "myadmin:wait"
                    },
                    {
                        "name": "菜单管理",
                        "url": "myadmin:menu_list"
                    },
                    {
                        "name": "个人信息",
                        "url": "myadmin:wait"
                    }
                ]
            }

        ]
        return render(request, 'myadmin/index.html', context={'menus': menus})

class HomeView(View):
    def get(self, request):
        return render(request, 'myadmin/home.html')


class WaitView(View):
    def get(self, request):
        return render(request, 'myadmin/wait.html')


class MenuListView(View):
    """
    菜单列表
    url:/admin/menus/
    """
    def get(self, request):
        # 拿到所有的一级菜单
        menus = Menu.objects.only('name', 'url', 'icon', 'is_visible', 'order', 'codename', 'is_delete').filter(parent=None)

        return render(request, 'myadmin/menu/menu_list.html', context={'menus': menus})


class MenuAddView(View):
    """
    添加菜单视图
    url:/admin/menu/
    """
    def get(self, request):
        form = MenuModelForm()
        return render(request, 'myadmin/menu/add_menu.html', context={'form': form})

    def post(self, request):
        # 1. 接受参数并验证
        form = MenuModelForm(request.POST)
        if form.is_valid():
            # 创建菜单
            new_menu = form.save()
            # 菜单的权限对象
            content_type = ContentType.objects.filter(app_label='myadmin', model='menu').first()
            permission = Permission.objects.create(name=new_menu.name, content_type=content_type, codename=new_menu.codename)
            new_menu.permission = permission
            new_menu.save(update_fields=['permission'])

            return json_response(errmsg='菜单添加成功！')
        else:
            return render(request, 'myadmin/menu/add_menu.html', context={'form': form})


class MenuUpdateView(View):
    """
    url:myadmin/menu/<int:menu_id>/
    """
    def delete(self,request,menu_id):
        menu = Menu.objects.filter(id = menu_id).only('name')
        if menu:
            menu = menu[0]
            #查看是否是父菜单
            if menu.children.filter().exists():
                return json_response(errno=Code.DATAERR,errmsg='父菜单非空不能删除')
            menu.permission.delete()
            return json_response(errmsg='父菜单：%s删除成功'%menu.name)
        else:
            return json_response(errno=Code.NODATA,errmsg='菜单不存在，因此不能删除')

    def get(self,request,menu_id):
        menu = Menu.objects.filter(id = menu_id).first()
        form = MenuModelForm(instance=menu)
        return render(request,'myadmin/menu/update_menu.html',context={'form':form})

    def put(self,request,menu_id):
        menu = Menu.objects.filter(id = menu_id).first()
        if not menu:
            return json_response(errno=Code.NODATA,errmsg='菜单不存在')
        #获取put请求的参数
        put_data = QueryDict(request.body)
        form = MenuModelForm(put_data,instance=menu)
        if form.is_valid():
            obj = form.save()
            #检查修改了的字段是否和权限有关
            flag = False
            if 'name'in form.changed_data:
                #返回一个修改了的权限的列表
                obj.permission.name = obj.name
                flag = True
            if 'codename'in form.changed_data:
                obj.permission.codename = obj.codename
                flag = True
            if flag:
                obj.permission.save()
            return json_response(errmsg='菜单修改成功')
        else:
            return render(request,'myadmin/menu/update_menu.html',context={'form':form})
