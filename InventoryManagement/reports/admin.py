from django.contrib import admin
from .models import SalesReport, SalesDetail, CustomerReport
from sales.models import Order
from django.utils import timezone

# Register your models here.


class SalesDetailInline(admin.TabularInline):
    model = SalesDetail
    extra = 0
    readonly_fields = ()


class SalesReportAdmin(admin.ModelAdmin):

    inlines = [SalesDetailInline]

    @admin.action(description='Generate sales report')
    def generate_report_for_all_data(self, request, queryset):
        total_sales = 0
        for order in Order.objects.all():
            total_sales += order.total_price

        report = SalesReport.objects.create(
            report_date=timezone.now(),
            total_sales=total_sales,
            generated_by=request.user.username
        )

        self.message_user(request, "Sales report for all data generated successfully.")

    actions = [generate_report_for_all_data]


class CustomerReportAdmin(admin.ModelAdmin):

    @admin.action(description='Generate customer report')
    def generate_customer_report(self, request, queryset):
        for customer in queryset:
            report = CustomerReport(customer=customer)
            report.generate_report()
            self.message_user(request, f'Report generated for {customer}')

    actions = [generate_customer_report]


admin.site.register(SalesReport, SalesReportAdmin)
admin.site.register(CustomerReport,CustomerReportAdmin)
