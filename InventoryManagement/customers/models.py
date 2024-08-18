from django.db import models

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(blank=True)
    address = models.TextField(blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PurchaseHistory(models.Model):
    # Linking purchase history to a specific Customer
    customer = models.ForeignKey(Customer, related_name='purchase_history', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    purchase_date = models.DateTimeField(auto_now_add=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} bought by {self.customer} on {self.purchase_date}'

    class Meta:
        verbose_name_plural = "Purchase History"
