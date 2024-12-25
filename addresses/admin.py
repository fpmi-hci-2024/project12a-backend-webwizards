from django.contrib import admin

from addresses.models import City, Address


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_region_display','slug')
    search_fields = ('name',)
    list_filter = ('region',)
    ordering = ('name',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'name')
    search_fields = ('name',)
    list_filter = ('city',)
    ordering = ('city', 'name')


admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
