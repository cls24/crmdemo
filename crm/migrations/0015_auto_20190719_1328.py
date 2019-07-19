# Generated by Django 2.2.3 on 2019-07-19 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_auto_20190719_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key='ordernum', related_name='order', serialize=False, to='crm.CustomerOrder'),
        ),
    ]