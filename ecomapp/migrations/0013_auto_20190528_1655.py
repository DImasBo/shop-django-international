# Generated by Django 2.2.1 on 2019-05-28 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0012_property_propertyimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyimage',
            name='property',
        ),
        migrations.DeleteModel(
            name='Property',
        ),
        migrations.DeleteModel(
            name='PropertyImage',
        ),
    ]
