import time

from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from .models import Wallet, Operation, Log
from rest_framework.exceptions import NotFound, ValidationError
from .serializers import WalletSerializer, OperationSerializer
from django.db import transaction, IntegrityError

from .utils import execute_tansaction


class wallet_operation(generics.CreateAPIView):
    serializer_class = OperationSerializer

    def post(self, request, *args, **kwargs):
        wallet_uuid = kwargs.get('WALLET_UUID')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            execute_tansaction(data=serializer.validated_data, wal=wallet_uuid)
        print(serializer.validated_data)
        return HttpResponse(status=200)


class wallet_detail(generics.RetrieveAPIView):
    lookup_url_kwarg = 'WALLET_UUID'
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get(self, request, *args, **kwargs):
        time.sleep(1)
        return super().get(request, *args, **kwargs)
# class WalletApiView(mixins.RetrieveModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer
#     lookup_field = 'uuid'
#
#
# class OperationViewSet(mixins.CreateModelMixin,
#                        viewsets.GenericViewSet):
#     serializer_class = OperationSerializer
#
#     def get_wallet(self):
#         wallet_pk = self.kwargs.get('wallet_uuid')
#         try:
#             return Wallet.objects.get(uuid=wallet_pk)
#         except Wallet.DoesNotExist:
#             raise NotFound("Wallet not found")
#
#     def perform_create(self, serializer):
#         wallet = self.get_wallet()
#         data = serializer.validated_data
#
#         op_type = data['operation_type'].upper()
#         amount = data['amount']
#
#         if op_type == 'WITHDRAW':
#             if wallet.balance < amount:
#                 log_msg = f"Balance. Tried to withdraw {amount} from wallet {wallet.pk}"
#                 log = Log.objects.create(message=log_msg)
#                 raise ValidationError("Insufficient funds")
#             wallet.balance -= amount
#             log_msg = f"Operation. Withdraw {amount} from wallet {wallet.pk}"
#             log = Log.objects.create(message=log_msg)
#         elif op_type == 'DEPOSIT':
#             wallet.balance += amount
#             log_msg = f"Operation. Deposit {amount} to wallet {wallet.pk}"
#             log = Log.objects.create(message=log_msg)
#         else:
#             log_msg = f"Invalid. Tried {op_type} operation to wallet {wallet.pk}"
#             log = Log.objects.create(message=log_msg)
#             raise ValidationError("Invalid operation type")
#
#         try:
#             with transaction.atomic():
#                 serializer.save(wallet_uuid_id=wallet.uuid, operation_type=op_type, log=log)
#                 wallet.save()
#         except IntegrityError as e:
#             log_msg = f"IntegrityError while updating wallet {wallet.uuid}: {e}"
#             log = Log.objects.create(message=log_msg)
#         except Exception as e:
#             log_msg = f"Error while updating wallet {wallet.uuid}: {e}"
#             log = Log.objects.create(message=log_msg)
#         else:
#             log_msg = f"Operation succsess"
#             log = Log.objects.create(message=log_msg)
