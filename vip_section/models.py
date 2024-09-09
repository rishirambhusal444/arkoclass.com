from django.db import models
from django.utils import timezone
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255, unique=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_code = models.CharField(max_length=255, null=True, blank=True)
    transaction_uuid = models.CharField(max_length=255, null=True, blank=True)
    transaction_status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')])

    total_amount = models.FloatField(null=True, blank=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)  # Name of the product
    product_code = models.CharField(max_length=255, null=True, blank=True)  # Product code
    payment_gateway = models.CharField(max_length=50, blank=True, null=True)  # Payment method
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Order {self.order_id} - {self.transaction_status}"


from django.db import models
from django.contrib.auth.models import User

class OfflinePayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    payment_proof = models.ImageField(upload_to='payment_proofs/')

    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment from {self.email} for Subject ID {self.subject_id}'

