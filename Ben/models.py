from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    ccp=models.IntegerField()
    numCard=models.IntegerField()
    willaya=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prix_Achat=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    remise = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    created_at = models.DateTimeField(default=timezone.now)
    installment_period = models.IntegerField(default=10)  # Number of installments
    init_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_dub=models.DateTimeField()

    def __str__(self):
        return f"Invoice #{self.pk} - {self.customer.name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='invoice_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # def save(self, *args, **kwargs):
    #     self.total_price = self.product.price * self.quantity
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment for Invoice #{self.invoice.pk} - {self.amount}"
