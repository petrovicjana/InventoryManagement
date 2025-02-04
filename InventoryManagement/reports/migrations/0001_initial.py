# Generated by Django 5.1 on 2024-08-17 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0004_remove_purchasehistory_status'),
        ('inventory', '0003_stockhistory_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateTimeField(auto_now_add=True)),
                ('total_sales', models.DecimalField(decimal_places=2, max_digits=10)),
                ('generated_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateTimeField(auto_now_add=True)),
                ('report_content', models.TextField()),
                ('total_spent', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('number_of_orders', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='SalesDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sold', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='reports.salesreport')),
            ],
        ),
    ]
