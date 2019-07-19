# Generated by Django 2.2.3 on 2019-07-19 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_delete_orderlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productnum', models.IntegerField(default=1)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.CustomerOrder')),
                ('pm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ProductModel')),
            ],
        ),
    ]
