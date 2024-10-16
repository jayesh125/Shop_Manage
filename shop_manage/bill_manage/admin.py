from django.contrib import admin
from .models import Bill, BillProduct

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'customer', 'total_amount', 'gst_amount', 'discount', 'payment_status')

@admin.register(BillProduct)
class BillProductAdmin(admin.ModelAdmin):
    list_display = ('bill', 'product', 'quantity', 'price')
