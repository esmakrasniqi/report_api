# Generated by Django 4.0.2 on 2022-02-07 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0005_alter_task_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='taskId',
        ),
        migrations.AddField(
            model_name='task',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
