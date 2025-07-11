# Generated by Django 5.1.4 on 2025-03-26 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_alter_rentorder_delivery_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentorder',
            name='delivery_person',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'Delivery Person'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_assignments', to='myapp.employee'),
        ),
        migrations.AlterField(
            model_name='rentorder',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Assigned', 'Assigned'), ('Delivered', 'Delivered'), ('Returned', 'Returned')], default='Pending', max_length=20),
        ),
    ]
