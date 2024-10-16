from rest_framework import serializers
from .models import Bill, BillProduct
from product_manage.models import Product
from customer_manage.models import Customer

class BillProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillProduct
        fields = ['product', 'quantity', 'price', 'gst_applicable']


class BillSerializer(serializers.ModelSerializer):
    bill_products = BillProductSerializer(many=True, write_only=True)

    class Meta:
        model = Bill
        fields = ['bill_number', 'customer', 'total_amount', 'discount', 'gst_amount', 'payment_status', 'bill_products']

    def create(self, validated_data):
        products_data = validated_data.pop('bill_products')
        bill = Bill.objects.create(**validated_data)
        
        # Initialize total_amount to calculate
        total_amount = 0

        # Loop through bill_products
        for product_data in products_data:
            # Fetch product object
            product = Product.objects.get(id=product_data['product'].id)
            
            # Use the provided price or fall back to the product's price from the Product model
            price = product_data.get('price', product.price)
            quantity = product_data['quantity']
            
            # Check if enough stock is available
            if product.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock for product {product.name}")
            
            # Update product quantity
            product.quantity -= quantity
            product.save()

            # Create BillProduct instance
            BillProduct.objects.create(
                bill=bill,
                product=product,
                quantity=product_data['quantity'],
                price=price,
                gst_applicable=product_data.get('gst_applicable', True)
            )

            # Add to total amount
            total_amount += price * product_data['quantity']

        # Calculate GST (assuming 18% GST)
        gst_amount = total_amount * 18 / 100
        bill.total_amount = total_amount
        bill.gst_amount = gst_amount
        bill.save()

        # Access the related customer
        customer = bill.customer
        
        # Update paid_amount or unpaid_amount based on payment_status
        if bill.payment_status == 'Paid':
            customer.paid_amount += bill.total_amount
        else:
            customer.non_paid_amount += bill.total_amount

        # Save the customer with the updated amounts
        customer.save()

        

        return bill
