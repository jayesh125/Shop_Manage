from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'paid_amount', 'non_paid_amount']
        read_only_fields = ['paid_amount', 'non_paid_amount']

        def validate_phone(self, value):
            if not value.isdigit() or len(value) != 10:
                raise serializers.ValidationError("Invalid phone number. It should be a 10-digit number.")
            return value
        
        def validate_address(self, value):
            if len(value) < 5:
                raise serializers.ValidationError("Address should be at least 5 characters long.")
            return value
        
        def validate_paid_amount(self, value):
            if value < 0:
                raise serializers.ValidationError("Paid amount should not be negative.")
            return value
        
        def validate_non_paid_amount(self, value):
            if value < 0:
                raise serializers.ValidationError("Non-paid amount should not be negative.")
            return value
        
        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.address = validated_data.get('address', instance.address)
            instance.paid_amount = validated_data.get('paid_amount', instance.paid_amount)
            instance.non_paid_amount = validated_data.get('non_paid_amount', instance.non_paid_amount)
            instance.save()
            return instance
        
        def create(self, validated_data):
            return Customer.objects.create(**validated_data)
        
        