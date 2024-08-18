from django.contrib import admin
from .models import Customer, PurchaseHistory

# Register your models here.


class PurchaseHistoryInline(admin.TabularInline):
    # Specifying Inline class that should be displayed on the admin page for the Customer
    model = PurchaseHistory
    extra = 0
    readonly_fields = ('product_name', 'purchase_date', 'amount_spent')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'joined_date']
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('joined_date', )  # Filtering customers by the date they joined
    inlines = [PurchaseHistoryInline]


admin.site.register(Customer, CustomerAdmin)
