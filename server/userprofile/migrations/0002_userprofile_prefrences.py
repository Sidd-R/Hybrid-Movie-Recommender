# Generated by Django 5.1.3 on 2024-11-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='prefrences',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]