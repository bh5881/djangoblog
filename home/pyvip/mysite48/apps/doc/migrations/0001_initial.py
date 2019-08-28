# Generated by Django 2.1.1 on 2019-08-26 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('file_url', models.URLField(help_text='文件url', verbose_name='文件url')),
                ('file_name', models.CharField(help_text='文件名', max_length=48, verbose_name='文件名')),
                ('title', models.CharField(help_text='文件标题', max_length=150, verbose_name='文件标题')),
                ('image_url', models.URLField(help_text='分明面图片url', verbose_name='封面图片URL')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
