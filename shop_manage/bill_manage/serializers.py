from rest_framework import serializers
from .models import Bill, BillProduct
from product_manage.models import Product
from customer_manage.models import Customer

class BillProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillProduct
        fields = ['product', 'quantity', 'price']


class BillSerializer(serializers.ModelSerializer):
    bill_products = BillProductSerializer(many=True, write_only=True)
    low_stock_alerts = serializers.ListField(read_only=True)

    class Meta:
        model = Bill
        fields = ['bill_number', 'customer', 'total_amount', 'discount', 'gst_amount', 'payment_status', 'bill_products', 'low_stock_alerts']

    def create(self, validated_data):
        products_data = validated_data.pop('bill_products')
        bill = Bill.objects.create(**validated_data)
        
        total_amount = 0
        bill_product_objects = []
        low_stock_alerts = []

        for product_data in products_data:
            product = Product.objects.get(id=product_data['product'].id)
            price = product_data.get('price', product.price)
            quantity = product_data['quantity']

            if product.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock for product {product.name}")
            
            # Update product quantity and check stock alert
            product.quantity -= quantity
            product.save()

            if product.quantity < product.low_stock_threshold:
                low_stock_alerts.append(f"Low stock alert for {product.name}: Only {product.quantity} left.")

            # Create BillProduct instances to be bulk inserted later
            bill_product_objects.append(BillProduct(
                bill=bill,
                product=product,
                quantity=quantity,
                price=price,
                gst_amount=price * quantity * 18 / 100  # Calculate GST per product
            ))

            total_amount += price * quantity

        BillProduct.objects.bulk_create(bill_product_objects)

        # Update bill total and GST
        gst_amount = total_amount * 18 / 100
        bill.total_amount = total_amount
        bill.gst_amount = gst_amount
        bill.save()

        customer = bill.customer
        if bill.payment_status == 'Paid':
            customer.paid_amount += bill.total_amount
        else:
            customer.non_paid_amount += bill.total_amount
        customer.save()

        bill.low_stock_alerts = low_stock_alerts
        return bill
