import time
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from .utils import execute_tansaction

request_schema_dict = openapi.Schema(
    title="Execute operation",
    type=openapi.TYPE_OBJECT,
    properties={
        'operation_type': openapi.Schema(type=openapi.TYPE_STRING, example="DEPOSIT|WITHDRAW"),
        'amount': openapi.Schema(type=openapi.TYPE_STRING, example="15"),
    }
)


class wallet_operation(generics.CreateAPIView):
    serializer_class = OperationSerializer

    @swagger_auto_schema(request_body=request_schema_dict,
                         responses={201: openapi.Schema(title="Response", type=openapi.TYPE_OBJECT, properties={
                             "operation_type": openapi.Schema(type=openapi.TYPE_STRING, example="DEPOSIT|WITHDRAW"),
                             "amount": openapi.Schema(type=openapi.TYPE_STRING, example="15")}),
                                    400: "Error: Bad Request"},
                         operation_description="Выполнение операции зачисления или списания средств с электронного кошелька")
    def post(self, request, *args, **kwargs):
        wallet_uuid = kwargs.get('WALLET_UUID')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            execute_tansaction(data=serializer.validated_data, wal=wallet_uuid)
        return HttpResponse(status=201, content=str(serializer.validated_data))


class wallet_detail(generics.RetrieveAPIView):
    lookup_url_kwarg = 'WALLET_UUID'
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @swagger_auto_schema(responses={
        200: WalletSerializer,
        404: openapi.Schema(title="Response", type=openapi.TYPE_OBJECT,
                            properties={"detail": openapi.Schema(type=openapi.TYPE_STRING,
                                                                 example="No Wallet matches the given query")})},
        operation_description="Получение информации о кошельке")
    def get(self, request, *args, **kwargs):
        time.sleep(1)
        return super().get(request, *args, **kwargs)
