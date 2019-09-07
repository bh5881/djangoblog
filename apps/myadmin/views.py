from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.core.paginator import Paginator
from .models import Menu
from user.models import User
from .forms import MenuModelForm,UserModelForm,GroupModelForm
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
        #拿到所有的可用，可见菜单，一级菜单
        objs = Menu.objects.only('name','url','icon','permission__codename','permission__content_type__app_label').select_related('permission__content_type').filter(is_delete=False,is_visible=True,parent=None)
 #过滤用户拥有权限的菜单
        has_permissions = request.user.get_all_permissions()
        #3构造数据结构
        menus = []
        for menu in objs:
            if '%s.%s'%(menu.permission.content_type.app_label,menu.permission.codename)in has_permissions:
                temp = {'name':menu.name,
                        'icon':menu.icon}
                #检查是否有可用可见的子菜单
                children = menu.children.filter(is_delete=False,is_visible=True)
                if children:
                    temp['children'] = []
                    for child in children:
                        if '%s.%s'%(child.permission.content_type.app_label,child.permission.codename) in has_permissions:
                            temp['children'].append({'name':child.name,'url':child.url})
                else:
                    if not menu.url:
                        continue
                    temp['url'] = menu.url
                menus.append(temp)
        return render(request,'myadmin/index.html',context ={'menus':menus})



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

class UserListView(View):
    """
    用户里列表视图
    url:/myadmin/users/
    """
    def get(self,request):
        #1,获取用户的查询集
        user_queryset = User.objects.only('username','is_active','mobile','is_staff','is_superuser')
        groups = Group.objects.only('name')
            #2,接收参数并校验，过滤字典
        query_dict = {}
        groups__id=request.GET.get('group')
        if groups__id:
            try:
                groups__id = int(groups__id)
                query_dict['groups__id'] = groups__id
            except Exception as e:
                pass
        is_staff = request.GET.get('is_staff')
        if is_staff =='0':
            query_dict['is_staff'] = False
        if is_staff == '1':
            query_dict['is_staff'] = True
        is_superuser = request.GET.get('is_superuser')
        if is_superuser =='0':
            query_dict['is_superuser'] = False
        if is_superuser =='1':
            query_dict['is_superuser'] = True
        username = request.GET.get('username')
        if username:
            query_dict['username'] = username
        #过滤分页
        try:
            page = int(request.GET.get('page',1))
        except Exception as e:
            page = 1
        paginator = Paginator(user_queryset.filter(**query_dict),4)
        users = paginator.get_page(page)
        #5,渲染模板
        context = {'users':users,'groups':groups}
        context.update(query_dict)
        #返回
        return render(request,'myadmin/user/user_list.html',context=context)

class UserUpdateView(View):
    """
    用户更新视图
    url:/myadmin/user/<int:user_id>
    """
    def get(self,request,user_id):
        user = User.objects.filter(id = user_id).first()
        if user:
            form = UserModelForm(instance = user)
        else:
            return json_response(errno=Code.NODATA,errmsg='没有此用户')
        return render(request,'myadmin/user/user_detail.html',context={'form':form})

    def put(self,request,user_id):
        #1,拿到要修改的用户对象
        user = User.objects.filter(id =user_id).first()
        #2.判断用户是否存在
        if not user:
            return json_response(errno=Code.NODATA,errmsg='没有此用户')
        #2拿到前端传递的参数
        put_data = QueryDict(request.body)
        #校验参数
        #3.1创建表单对象
        form = UserModelForm(put_data,instance= user)
        if form.is_valid():
    #4,如果修改成功，保存表单数据
            form.save()
            return json_response(errmsg='用户修改成功了！！！')
        else:
            return render(request,'myadmin/user/user_detail.html',context ={'form':form})




