# Generated by Django 5.1.6 on 2025-03-14 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_assign_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='assigned_task',
        ),
    ]
