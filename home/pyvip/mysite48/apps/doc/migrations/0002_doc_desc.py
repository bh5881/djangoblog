# Generated by Django 2.1.1 on 2019-08-26 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='desc',
            field=models.TextField(default=1, help_text='文件描述', verbose_name='文件描述'),
            preserve_default=False,
        ),
    ]
