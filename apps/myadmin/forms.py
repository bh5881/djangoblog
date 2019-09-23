# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝 2019/8/29 21:37

from django import forms
from django.contrib.auth.models import Group,Permission
from .models import Menu
from user.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from news.models import News , Tag

class MenuModelForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=None, required=False , label='父菜单')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Menu.objects.filter(is_delete=False, is_visible=True, parent=None)

    class Meta:
        model = Menu
        fields = ['name', 'url', 'order', 'parent', 'icon', 'codename', 'is_visible']

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','mobile','is_staff','is_superuser','is_active','groups']


class GroupModelForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=None,required=False,help_text='权限',label='权限')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['permissions'].queryset = Permission.objects.filter(menu__is_delete=False)

    class Meta:
        model = Group
        fields  = ['name','permissions']


class NewsModelForm(forms.ModelForm):
    tag = forms.ModelChoiceField(queryset=None, required=False, help_text='分类', label='分类')
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='内容')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.filter(is_delete=False)

    class Meta:
        model = News
        fields = ['title', 'is_delete', 'digest', 'image_url', 'tag', 'content']