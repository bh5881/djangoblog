# Generated by Django 2.1.1 on 2019-09-02 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='父菜单', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='myadmin.Menu'),
        ),
    ]
