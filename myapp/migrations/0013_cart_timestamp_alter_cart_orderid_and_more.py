# Generated by Django 5.1.4 on 2025-03-26 05:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_customizeproduct_budget_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='timeStamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='orderid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='orderstatus',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='finalorders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=15)),
                ('total_amount', models.FloatField()),
                ('o_date', models.DateField(auto_now_add=True)),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userlogin')),
            ],
            options={
                'verbose_name_plural': 'order',
            },
        ),
        migrations.CreateModel(
            name='FinalOrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_type', models.CharField(choices=[('online', 'Online Payment'), ('offline', 'Offline Payment')], max_length=10)),
                ('amount', models.FloatField()),
                ('razorpay_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('offline_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('offline_remarks', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed'), ('Not Paid', 'Not Paid')], default='Pending', max_length=20)),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userlogin')),
                ('o_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.finalorders')),
            ],
            options={
                'verbose_name_plural': 'payment',
            },
        ),
    ]
