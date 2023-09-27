# Generated by Django 4.2.4 on 2023-09-04 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_userdata_address_alter_userdata_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='address',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
