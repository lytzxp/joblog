# Generated by Django 3.1.4 on 2021-02-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_topic_is_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='is_publish',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
