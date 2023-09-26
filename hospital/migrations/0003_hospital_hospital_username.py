# Generated by Django 3.2.3 on 2021-07-01 17:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_hospital_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='hospital_username',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
