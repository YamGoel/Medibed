# Generated by Django 3.2.3 on 2021-07-04 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
