from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, CategoryProductsAPIView, ReviewView

urlpatterns = [
    path('categories/<slug:slug>/', CategoryProductsAPIView.as_view(), name='category-products'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/<int:product_id>/reviews/', ReviewView.as_view(), name='product-reviews'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
]