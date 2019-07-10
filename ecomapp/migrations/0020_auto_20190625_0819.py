# Generated by Django 2.2.2 on 2019-06-25 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0019_auto_20190624_1438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery',
        ),
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('nova_poshta', 'Нова пошта'), ('ukr_poshta', 'Укр-пошта')], max_length=40),
        ),
    ]
