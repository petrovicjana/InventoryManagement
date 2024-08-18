from django.contrib import admin
from .models import Product, StockHistory

# Register your models here.
admin.site.site_header = 'Inventory Management'


class StockHistoryInline(admin.TabularInline):
    model = StockHistory
    extra = 0
    readonly_fields = ['product', 'change', 'date']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'stock_level']
    search_fields = ('name', 'sku')
    actions = ['restock_products', 'reduce_stock_level']
    inlines = [StockHistoryInline]

    @admin.action(description='Re-stock selected products')
    def restock_products(modeladmin, request, queryset):
        """Re-stocking the selected products"""
        for product in queryset:
            product.restock(10)
        modeladmin.message_user(request, "Selected products have been restocked")

    @admin.action(description='Reduce stock of selected products')
    def reduce_stock_level(modeladmin,  request, queryset):
        """Reducing the stock of selected products"""
        for product in queryset:
            try:
                product.reduce_stock(10)
            except ValueError as e:
                modeladmin.message_user(request, str(e), level='error')
        modeladmin.message_user(request, "Stock has been reduced")


admin.site.register(Product, ProductAdmin)





