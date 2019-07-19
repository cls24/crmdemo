# Generated by Django 2.2.3 on 2019-07-19 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20190718_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='id',
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key='ordernum', serialize=False, to='crm.CustomerOrder'),
        ),
    ]
