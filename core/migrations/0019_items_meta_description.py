# Generated by Django 2.2.13 on 2021-07-28 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_items_meta_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='meta_description',
            field=models.CharField(default='No meta-description', help_text='Content for description meta tag', max_length=255),
            preserve_default=False,
        ),
    ]
