# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝 2019/8/29 21:37

from django import forms

from .models import Menu


class MenuModelForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=None, required=False , label='父菜单')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Menu.objects.filter(is_delete=False, is_visible=True, parent=None)

    class Meta:
        model = Menu
        fields = ['name', 'url', 'order', 'parent', 'icon', 'codename', 'is_visible']
