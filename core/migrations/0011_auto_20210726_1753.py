# Generated by Django 2.2.13 on 2021-07-26 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210726_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='countries',
            new_name='country',
        ),
    ]
