# Generated by Django 4.2.4 on 2023-09-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_userdata_address_alter_userdata_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='address',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='postal_code',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]
