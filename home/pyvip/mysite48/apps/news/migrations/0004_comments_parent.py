# Generated by Django 2.1.1 on 2019-08-27 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_comments_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.Comments'),
        ),
    ]
