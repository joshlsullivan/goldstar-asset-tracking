# Generated by Django 2.0.1 on 2018-02-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_task_time_difference',
        ),
        migrations.AddField(
            model_name='task',
            name='job_task_time_difference',
            field=models.CharField(default='', max_length=80),
            preserve_default=False,
        ),
    ]
