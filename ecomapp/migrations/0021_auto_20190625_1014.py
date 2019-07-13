# Generated by Django 2.2.2 on 2019-06-25 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0020_auto_20190625_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=255, verbose_name='адреса'),
        ),
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('nova_poshta', 'Нова пошта'), ('ukr_poshta', 'Укр-пошта')], max_length=40, verbose_name='Спосіб доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Коментарь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Електрона пошта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=200, verbose_name='Імя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=200, verbose_name='Побатькові'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=9, verbose_name='Номер телефона +380'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='ecomapp.Product', verbose_name='Товари'),
        ),
        migrations.AlterField(
            model_name='order',
            name='second_name',
            field=models.CharField(max_length=200, verbose_name='Прізвище'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('AIP_status', 'Прийнятий в обробку'), ('IP_status', 'В обробці'), ('PAID_status', 'Оплачено')], default='AIP_status', max_length=100, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Сума'),
        ),
    ]