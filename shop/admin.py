from django.contrib import admin

from shop.models import Category, Product, Review, Profile


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'profile', 'rating', 'created', 'updated']
    list_filter = ['rating', 'created']
    readonly_fields = ['created', 'updated']


admin.site.register(Review, ReviewAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city']
    search_fields = ['user__username']


admin.site.register(Profile, ProfileAdmin)
