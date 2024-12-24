from django.db.models import Q
from drf_spectacular import openapi
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter, OpenApiExample, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Review
from .models import Product
from .serializers import CategorySerializer, ProductFilterSerializer, ReviewSerializer
from .serializers import ProductSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получение списка категорий",
        description="Получить список всех доступных категорий.",
        responses={
            200: CategorySerializer(many=True),
        },
    ),
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(
    get=extend_schema(
        summary="Получение всех доступных товаров (с возможностью поиска)",
        description="Получить все доступные товары. Можно использовать параметр `search` для фильтрации товаров по имени или описанию.",
        parameters=[
            OpenApiParameter('search', str, description='Поисковая строка для фильтрации товаров')
        ],
        responses={
            200: ProductSerializer(many=True),
        },
    ),
)
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary="Получение информации о товаре",
        description="Получить подробную информацию о продукте по его ID.",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(
                response=None,
                description='Товар не найден'),
        },
    ),
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


@extend_schema_view(
    get=extend_schema(
        summary="Получение продуктов по категории (с возможностью фильтрации)",
        description="Получить список продуктов в указанной категории. Поддерживаются фильтры по цене, производителям и году выпуска.",
        parameters=[
            OpenApiParameter('min_price', int, description="Минимальная цена продукта", required=False),
            OpenApiParameter('max_price', int, description="Максимальная цена продукта", required=False),
            OpenApiParameter('manufacturers', str, description="Список производителей", required=False),
            OpenApiParameter('min_year', int, description="Минимальный год выпуска продукта", required=False),
            OpenApiParameter('max_year', int, description="Максимальный год выпуска продукта", required=False),
        ],
        responses={
            200: ProductSerializer(many=True),
            404: OpenApiResponse(
                response=None,
                description="Продукты не найдены для этой категории."
            ),
        },
    ),
)
class CategoryProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        queryset = self.queryset.filter(category__slug=category_slug)

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        manufacturers = self.request.query_params.getlist('manufacturers')
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        if manufacturers:
            queryset = queryset.filter(manufacturer__in=manufacturers)

        if min_year is not None:
            queryset = queryset.filter(release_year__gte=min_year)
        if max_year is not None:
            queryset = queryset.filter(release_year__lte=max_year)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Продукты не найдены для этой категории."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="Получение отзывов о продукте",
        description="Получить список отзывов для указанного продукта. Если отзывы отсутствуют, будет возвращено сообщение об ошибке.",
        responses={
            200: ReviewSerializer(many=True),
            404: OpenApiResponse(
                response=None,
                description="Отзывы для этого продукта не найдены."
            ),
        },
    ),
    post=extend_schema(
        summary="Добавление отзыва на продукт",
        description="Создать новый отзыв для указанного продукта. Если отзыв уже существует от текущего пользователя, будет возвращено сообщение об ошибке.",
        responses={
            201: ReviewSerializer,
            400: OpenApiResponse(
                response=None,
                description="Ошибка валидации данных. Пользователь уже оставил отзыв."
            ),
        },
    ),
)
class ReviewListView(generics.GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product__id=product_id)

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"detail": "Отзывы для этого продукта не найдены."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        product_id = self.kwargs.get('product_id')

        if Review.objects.filter(product_id=product_id, profile=profile).exists():
            return Response({"detail": "Вы уже оставили отзыв на этот продукт."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile, product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    delete=extend_schema(
        summary="Удаление отзыва о продукте",
        description="Удалить отзыв пользователя о продукте. Если отзыв не найден, будет возвращено сообщение об ошибке.",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Отзыв успешно удален."
            ),
            404: OpenApiResponse(
                response=None,
                description="Отзыв не найден."
            ),
        },
    ),
)
class ReviewDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        profile = request.user.profile

        try:
            review = Review.objects.get(product__id=product_id, profile=profile)
        except Review.DoesNotExist:
            return Response({"detail": "Отзыв не найден."}, status=status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
