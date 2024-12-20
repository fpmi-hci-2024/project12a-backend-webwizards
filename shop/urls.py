from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, ProductFilterAPIView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/filter/', ProductFilterAPIView.as_view(), name='product-filter'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
]