from django.test import TestCase
from django.urls import reverse

from .models import Wallet

# Create your tests here.
class WalletViewTest(TestCase):
    number_of_wallets = 5
    @classmethod
    def setUpTestData(cls):
        for wallet in range(cls.number_of_wallets):
            Wallet.objects.create(balance=100)

    def test_wallets_list_view_accessible_by_name(self):
        response = self.client.get(reverse('wallets'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.number_of_wallets)

    def test_wallets_list_view_accessible_by_url(self):
        response = self.client.get('/api/v1/wallets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.number_of_wallets)

    def test_wallet_required_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('wallets'))
        wallet_uuid = response.json()[0]['uuid']
        response = self.client.get(f'/api/v1/wallets/{wallet_uuid}/')
        self.assertEqual(response.status_code, 200)

    def test_wallet_operation_view_DEPOSIT(self):
        response = self.client.get(reverse('wallets'))
        wallet_uuid = response.json()[0]['uuid']
        response = self.client.post(reverse('wallet_operation', kwargs={'WALLET_UUID': wallet_uuid}),
                                    data={'operation_type': 'DEPOSIT', 'amount': 100})
        self.assertEqual(response.status_code, 201)

    def test_wallet_operation_view_WITHDRAW(self):
        response = self.client.get(reverse('wallets'))
        wallet_uuid = response.json()[1]['uuid']
        response = self.client.post(reverse('wallet_operation', kwargs={'WALLET_UUID': wallet_uuid}),
                                    data={'operation_type': 'WITHDRAW', 'amount': 100})
        self.assertEqual(response.status_code, 201)

    def test_wallet_operation_view_WITHDRAW_insufficient_funds(self):
        response = self.client.get(reverse('wallets'))
        wallet_uuid = response.json()[2]['uuid']
        response = self.client.post(reverse('wallet_operation', kwargs={'WALLET_UUID': wallet_uuid}),
                                    data={'operation_type': 'WITHDRAW', 'amount': 1000})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()[0], 'Insufficient funds')