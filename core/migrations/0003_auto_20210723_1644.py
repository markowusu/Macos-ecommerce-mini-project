# Generated by Django 2.2.13 on 2021-07-23 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210723_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('Sw', 'ShirtWeater'), ('Ow', 'Outwear')], default='S', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='label',
            field=models.CharField(choices=[('p', 'primary'), ('S', 'secondary'), ('D', 'danger')], default='P', max_length=2),
            preserve_default=False,
        ),
    ]
