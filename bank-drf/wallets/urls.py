from django.urls import path
from . import views

urlpatterns = [
    path('<WALLET_UUID>/operation', views.wallet_operation.as_view(), name='wallet_operation'),
    path('<WALLET_UUID>', views.wallet_detail.as_view(), name='wallet_detail'),
]