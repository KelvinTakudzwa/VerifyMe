# Generated by Django 5.0.6 on 2024-07-03 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_userprofile_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employer',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='employee',
            name='year_started',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
