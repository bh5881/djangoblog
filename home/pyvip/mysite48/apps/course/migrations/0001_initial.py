# Generated by Django 2.1.1 on 2019-08-31 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('title', models.CharField(help_text='课程名', max_length=150, verbose_name='课程名')),
                ('cover_url', models.URLField(help_text='封面url', verbose_name='封面url')),
                ('video_url', models.URLField(help_text='课程视频url', verbose_name='课程视频url')),
                ('duration', models.DurationField(help_text='课程时长', verbose_name='课程时长')),
                ('profile', models.TextField(blank=True, help_text='课程简介', null=True, verbose_name='课程简介')),
                ('outline', models.TextField(blank=True, help_text='课程大纲', null=True, verbose_name='课程大纲')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
                'db_table': 'tb_course',
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('name', models.CharField(help_text='课程分类名', max_length=100, verbose_name='课程分类名')),
            ],
            options={
                'verbose_name': '课程分类',
                'verbose_name_plural': '课程分类',
                'db_table': 'tb_course_category',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('name', models.CharField(help_text='讲师姓名', max_length=150, verbose_name='讲师姓名')),
                ('title', models.CharField(help_text='职称', max_length=150, verbose_name='职称')),
                ('profile', models.TextField(help_text='简介', verbose_name='简介')),
                ('photo', models.URLField(default='', help_text='头像url', verbose_name='头像url')),
            ],
            options={
                'verbose_name': '讲师',
                'verbose_name_plural': '讲师',
                'db_table': 'tb_teachers',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.CourseCategory'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.Teacher'),
        ),
    ]
