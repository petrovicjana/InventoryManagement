from customers.models import Customer
from sales.models import Order
from inventory.models import Product
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.db.models import Sum

# Create your models here.


class SalesReport(models.Model):
    # Overview of total sales
    report_date = models.DateTimeField(auto_now_add=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    generated_by = models.CharField(max_length=100)  # Person that generated the report

    def __str__(self):
        return f'Report generated on {self.report_date}'

    def generate_report(self):
        """Generating sales report for all delivered orders"""

        total_sales = Order.objects.filter(status='delivered').aggregate(
            total=models.Sum('total_price')
        )['total'] or 0.00

        self.total_sales = total_sales
        self.save()


class SalesDetail(models.Model):
    # Providing detailed breakdown of sales at the product level
    report = models.ForeignKey(SalesReport, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()

    def __str__(self):
        return f'{self.quantity_sold} units of {self.product.name} sold'


class CustomerReport(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    report_content = models.TextField()
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_orders = models.IntegerField(default=0)

    def __str__(self):
        return f'Report for {self.customer} on {self.report_date}'

    def generate_report(self):
        """Calculating total spend by the costumer"""
        total_spent = Order.objects.filter(customer=self.customer, status='delivered').aggregate(
            total=models.Sum('total_price')
        )['total'] or 0.00

        # Calculate number of orders placed by the customer
        number_of_orders = Order.objects.filter(customer=self.customer, status='delivered').count()

        # Update the report with calculated data
        self.total_spent = total_spent
        self.number_of_orders = number_of_orders
        self.report_content = f'{self.customer} has placed {self.number_of_orders} orders, spending a total of {self.total_spent}.'
        self.save()

