# Generated by Django 2.2.1 on 2019-05-18 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0010_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=255)),
                ('buying_type', models.CharField(choices=[('self-checkout', 'самовивіз'), ('delivery', 'доставка')], max_length=40)),
                ('phone_number', models.CharField(max_length=9)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('status', models.CharField(choices=[('AIP_status', 'Прийнятий в обробку'), ('IP_status', 'В обробці'), ('PAID_status', 'Оплачено')], default='AIP_status', max_length=100)),
                ('comments', models.TextField(blank=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Cart')),
            ],
        ),
    ]