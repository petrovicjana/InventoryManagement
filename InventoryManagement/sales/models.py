from django.db import models
from customers.models import Customer, PurchaseHistory
from inventory.models import Product
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        if self.staff:
            return f'Order for {self.customer} handled by {self.staff} on {self.order_date}'
        return f'Order by {self.customer} on {self.order_date}'

    def save(self, *args, **kwargs):
        # Checking if this is an update and not a new order in order to restock items or create purchase history
        if self.pk:
            previous = Order.objects.get(pk=self.pk)

            # When order is delivered customer's purchase history is updated
            if previous.status != 'delivered' and self.status == 'delivered':
                self.create_purchase_history()

            # When order is cancelled product is restocked
            if previous.status != 'canceled' and self.status == 'canceled':
                self.restock_items()

        super().save(*args, **kwargs)

    def create_purchase_history(self):
        """Create purchase history records for each item in the order when delivered."""
        for item in self.items.all():
            PurchaseHistory.objects.create(
                customer=self.customer,
                product_name=item.product.name,
                purchase_date=self.order_date,
                amount_spent=item.get_total_price()
            )

    def restock_items(self):
        """Restock items when the order is canceled."""
        for item in self.items.all():
            item.product.restock(item.quantity)

    class Meta:
        verbose_name_plural = 'Order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_total_price(self):
        # Provide default values if quantity or price is None
        quantity = self.quantity if self.quantity is not None else 0
        price = self.price if self.price is not None else 0
        return quantity * price

    def save(self, *args, **kwargs):
        """Override save to reduce stock level when an OrderItem is created."""
        if self.pk is None:  # Reducing stock for new instances
            self.price = self.product.price
            super().save(*args, **kwargs)
            self.product.reduce_stock(self.quantity)
        else:
            super().save(*args, **kwargs)

    def reverse_stock(self):
        """Increase the stock level by the quantity of this item if the order is canceled."""
        self.product.restock(self.quantity)
