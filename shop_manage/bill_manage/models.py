from django.db import models, transaction
from django.utils import timezone
from customer_manage.models import Customer
from product_manage.models import Product

class Bill(models.Model):
    bill_number = models.CharField(max_length=15, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')

    def save(self, *args, **kwargs):
        if not self.bill_number:
            current_date = timezone.now().strftime('%Y%m%d')  # Example: '20241015'
            with transaction.atomic():
                
                last_bill = Bill.objects.filter(bill_number__startswith=f'BILL{current_date}').select_for_update().order_by('-bill_number').first()
                
                if last_bill:
                    # Extract and increment the last 4 digits of the last bill number
                    last_number = int(last_bill.bill_number[-4:])
                    new_number = last_number + 1
                else:
                    new_number = 1

                self.bill_number = f'BILL{current_date}{new_number:04d}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.bill_number} - {self.customer.name}"

class BillProduct(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='bill_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in Bill {self.bill.bill_number}"
