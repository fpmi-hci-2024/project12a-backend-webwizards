from django.contrib import admin

from users.models import Payment


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'payment_type', 'card_number', 'expiry_date']


admin.site.register(Payment, PaymentAdmin)
