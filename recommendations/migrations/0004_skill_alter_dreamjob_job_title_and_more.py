# Generated by Django 5.1.2 on 2024-10-31 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0003_remove_personalityprofile_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='dreamjob',
            name='job_title',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name='personalityprofile',
            name='skills',
        ),
        migrations.AlterField(
            model_name='personalityprofile',
            name='use_for_training',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='personalityprofile',
            name='skills',
            field=models.ManyToManyField(to='recommendations.skill'),
        ),
    ]
