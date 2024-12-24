from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, CategoryProductsAPIView, ReviewListView, \
    ReviewDetailView

urlpatterns = [
    path('categories/<slug:slug>/', CategoryProductsAPIView.as_view(), name='category-products'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review-list-create'),
    path('products/<int:product_id>/reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
]