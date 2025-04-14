from django.contrib import admin

from .models import Wallet, Operation

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    list_display = ('uuid', 'balance')


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Operation)
