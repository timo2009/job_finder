# Generated by Django 5.1.2 on 2024-10-31 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0002_remove_personalityprofile_current_job_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalityprofile',
            name='name',
        ),
    ]
