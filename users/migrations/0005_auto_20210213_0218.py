# Generated by Django 3.1.4 on 2021-02-13 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210213_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='ryimage',
            field=models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='ryimage'),
        ),
    ]
