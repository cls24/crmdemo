# Generated by Django 2.2.3 on 2019-07-19 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_auto_20190719_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='addtime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='ctime',
            field=models.DateTimeField(default='2019-07-19 09:23:29'),
        ),
    ]
