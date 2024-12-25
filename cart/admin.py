from django.contrib import admin

from cart.models import CartItem, Cart


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ['profile', 'created', 'updated']
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
