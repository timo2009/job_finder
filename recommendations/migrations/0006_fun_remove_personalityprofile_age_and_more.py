# Generated by Django 5.1.2 on 2024-10-31 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0005_interest_remove_personalityprofile_interests_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='personalityprofile',
            name='age',
        ),
        migrations.AddField(
            model_name='personalityprofile',
            name='funs',
            field=models.ManyToManyField(to='recommendations.fun'),
        ),
    ]