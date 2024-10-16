from django.contrib import admin
from customer_manage.models import Customer

# Register your models here.
@admin.register(Customer)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "paid_amount", "non_paid_amount", "user"]
    search_fields = ["name", "phone_number"]