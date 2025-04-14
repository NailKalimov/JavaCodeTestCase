from rest_framework import serializers
from .models import Wallet, Operation


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['uuid', 'balance']


class OperationSerializer(serializers.ModelSerializer):
    operation_type = serializers.CharField(write_only=True)
    amount = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Operation
        fields = ['operation_type', 'amount']

    def validate_operation_type(self, value):
        allowed = ['WITHDRAW', 'DEPOSIT']
        if value.upper() not in allowed:
            raise serializers.ValidationError(f"Operation must be one of {allowed}")
        return value.upper()  # нормализуем к верхнему регистру

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
