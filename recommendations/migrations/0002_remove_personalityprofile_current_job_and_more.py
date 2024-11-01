# Generated by Django 5.1.2 on 2024-10-31 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalityprofile',
            name='current_job',
        ),
        migrations.RemoveField(
            model_name='personalityprofile',
            name='job_satisfaction',
        ),
        migrations.RemoveField(
            model_name='personalityprofile',
            name='personality',
        ),
        migrations.AlterField(
            model_name='personalityprofile',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='DreamJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('satisfaction', models.IntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.personalityprofile')),
            ],
        ),
    ]