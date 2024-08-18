from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ()


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order_date', 'total_price', 'status']
    list_filter = ['status', 'order_date']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
