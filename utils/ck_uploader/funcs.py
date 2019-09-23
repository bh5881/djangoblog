# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝 2019/9/6 22:05

import os
from hashlib import md5


def get_filename(filename: str) -> str:
    suffix = filename.split('.')[-1]
    m = md5(os.urandom(16)+filename.encode('utf-8'))
    return m.hexdigest() + '.' + suffix


if __name__ == '__main__':
    print(get_filename('aa.txt'))