# Generated by Django 3.2.3 on 2021-11-04 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_items_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-name',), 'verbose_name': 'Category'},
        ),
    ]
