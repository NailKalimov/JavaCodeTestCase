from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Wallet, Operation


@transaction.atomic
def execute_tansaction(data, wal):
    wallet = Wallet.objects.select_for_update().get(uuid=wal)
    operation = Operation.objects.create(wallet_uuid=wallet, operation_type=data['operation_type'], amount=data['amount'])
    if operation.operation_type == 'WITHDRAW':
        if wallet.balance < operation.amount:
            raise ValidationError("Insufficient funds")
        wallet.balance -= operation.amount
    elif operation.operation_type == 'DEPOSIT':
        wallet.balance += operation.amount
    wallet.save()
    operation.save()