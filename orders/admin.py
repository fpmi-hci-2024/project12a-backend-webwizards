from django.contrib import admin

from orders.models import OrderItem, Order


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['product', 'quantity']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'status', 'created', 'updated', 'address', 'payment']
    list_filter = ['status', 'created']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
