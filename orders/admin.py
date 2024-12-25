from django.contrib import admin

from orders.models import OrderItem, Order


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Количество пустых форм для добавления новых OrderItem
    readonly_fields = ['product', 'quantity']  # Укажите поля, которые должны быть только для чтения

    def has_add_permission(self, request, obj=None):
        return False  # Запретить добавление новых OrderItem

    def has_change_permission(self, request, obj=None):
        return False  # Запретить изменение существующих OrderItem

    def has_delete_permission(self, request, obj=None):
        return False  # Запретить удаление OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'status', 'created', 'updated']
    list_filter = ['status', 'created']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
