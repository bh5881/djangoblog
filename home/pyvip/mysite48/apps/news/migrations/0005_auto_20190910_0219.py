# Generated by Django 2.1.1 on 2019-09-09 18:19

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_comments_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='内容', verbose_name='内容'),
        ),
    ]
