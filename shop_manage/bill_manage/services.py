def calculate_total(bill):
    total_amount = 0
    for bill_product in bill.bill_products.all():
        total_amount += bill_product.price * bill_product.quantity
    
    gst_amount = total_amount * 0.18  # Assuming 18% GST
    bill.total_amount = total_amount
    bill.gst_amount = gst_amount
    bill.save()
    return bill
