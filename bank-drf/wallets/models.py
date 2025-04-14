from django.db import models
import uuid

class Wallet(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    balance = models.DecimalField(max_digits=16, decimal_places=2)

class Operation(models.Model):
    wallet_uuid = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="operations")
    operation_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    log = models.ForeignKey('Log', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Log(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
