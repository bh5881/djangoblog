from django.db import models
# 需要导入这个文件
from django.contrib.auth.models import AbstractUser , UserManager as _UserManager

# 此处通过修改UserManager修改原UserManager函数，并且保留原函数的方法，就是面向对象
#用来修改creater_superuser 创建用户必须提供email 的行为
#下面添加管理器执行

class UserManager(_UserManager):
    def create_superuser(self, username,  password, email=None, **extra_fields):
        super().create_superuser(username=username, password=password, email=email, **extra_fields)

class User(AbstractUser):
    """
    继承abs的抽象模型，然后此处自定义自己的user模型
    此处添加mobile和email_active字段，或者更多的字段
    """
    mobile = models.CharField('手机号',max_length=11,unique=True,
                              help_text='手机号',error_messages={'unique':'此手机号已注册','max_length':'长度过长'})
    email_active = models.BooleanField('邮箱状态',default=False)
    class Meta:
        db_table= 'tb_user' #自定义表名
        verbose_name= '用户'
        verbose_name_plural = verbose_name #复数
    def __str__(self):
        return self.username
            #通过createsuperuser这个命令创建用的时候，需要的字段
    REQUIRED_FIELDS=['mobile'] #如果再写一个字段，就会提示输入另外一个字段
    #执行管理器
    object = UserManager()
#在settings里添加一句话说明User模型已被修改
# AUTH_USER_MODEL = 'user.User'