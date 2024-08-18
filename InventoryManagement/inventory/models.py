from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Returning the name and sku of desired product"""
        return f'{self.name}-{self.sku}'

    def restock(self, amount):
        """Increases stock level by the given amount and logs it to StockHistory"""
        self.stock_level += amount
        self.save()
        StockHistory.objects.create(product=self, change=amount)

    def reduce_stock(self, amount):
        """Reduces stock level by the given amount and logs it to StockHistory"""
        if amount > self.stock_level:
            raise ValueError("Not enough stock available!")
        self.stock_level -= amount
        self.save()
        StockHistory.objects.create(product=self, change=amount)


class StockHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    change = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.change} on {self.date} by {self.staff}'

    class Meta:
        verbose_name_plural = "Stock History"
