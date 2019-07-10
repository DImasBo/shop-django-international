# Generated by Django 2.2.1 on 2019-05-18 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0008_auto_20190517_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Cart'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('AIP_status', 'Прийнятий в обробку'), ('IP_status', 'В обробці'), ('PAID_status', 'Оплачено')], default='AIP_status', max_length=100),
        ),
    ]
