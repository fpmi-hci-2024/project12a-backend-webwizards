from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category
from .models import Product
from .serializers import CategorySerializer, ProductFilterSerializer
from .serializers import ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductFilterAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductFilterSerializer  # Use ProductFilterSerializer for input validation

    def post(self, request, *args, **kwargs):
        filter_serializer = self.get_serializer(data=request.data)
        if filter_serializer.is_valid():
            filters = filter_serializer.validated_data

            queryset = Product.objects.all()

            # Filter by price range
            min_price = filters.get('min_price')
            max_price = filters.get('max_price')
            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

            # Filter by manufacturers
            manufacturers = filters.get('manufacturers')
            if manufacturers:
                queryset = queryset.filter(manufacturer__in=manufacturers)

            # Filter by release year range
            min_year = filters.get('min_year')
            max_year = filters.get('max_year')
            if min_year is not None:
                queryset = queryset.filter(release_year__gte=min_year)
            if max_year is not None:
                queryset = queryset.filter(release_year__lte=max_year)

            # Serialize the filtered queryset
            product_serializer = ProductSerializer(queryset, many=True)
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)