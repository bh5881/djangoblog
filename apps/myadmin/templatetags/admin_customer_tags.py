# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝 2019/8/29 21:48
from django.template import Library

register = Library()


@register.simple_tag()
def add_class(field, class_str):
    return field.as_widget(attrs={'class': class_str})
