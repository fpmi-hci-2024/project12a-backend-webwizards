import logging

from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view, OpenApiParameter
from psycopg2 import IntegrityError
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from cart.models import Cart
from shop.models import Product, Profile
from shop.serializers import ProductSerializer, ProfileSerializer
from users.serializers import UserRegistrationSerializer, UserLoginSerializer

logger = logging.getLogger(__name__)

@extend_schema_view(
    post=extend_schema(
        summary="Регистрация пользователя",
        description="Создает нового пользователя и соответствующий профиль. Также создается корзина для пользователя.",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                response=None,
                description="Пользователь успешно зарегистрирован."
            ),
            400: OpenApiResponse(
                response=None,
                description="Ошибка валидации данных или имя пользователя/электронная почта уже заняты."
            ),
            500: OpenApiResponse(
                response=None,
                description="Неожиданная ошибка при регистрации пользователя."
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Регистрация нового пользователя",
                value={
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "password": "securepassword123",
                },
            ),
        ],
    ),
    get=extend_schema(
        summary="Получение профиля пользователя",
        description="Возвращает профиль аутентифицированного пользователя.",
        responses={
            200: OpenApiResponse(
                response=ProfileSerializer,
                description="Профиль пользователя успешно возвращен."
            ),
            403: OpenApiResponse(
                response=None,
                description="Пользователь не аутентифицирован."
            ),
        },
    ),
)
class UserProfileAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            user = serializer.create(serializer.initial_data)
            profile = Profile.objects.create(user=user)
            Cart.objects.create(profile=profile)

            logger.info(f"User registered successfully: {user.username} with profile: {profile.id}")
            return Response({'message': 'Пользователь успешно зарегистрирован!'}, status=status.HTTP_201_CREATED)

        except IntegrityError:
            logger.error("User registration failed: username or email already exists.")
            return Response({'error': 'Имя пользователя или электронная почта уже заняты.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("An unexpected error occurred during user registration.")
            return Response({'error': 'Произошла ошибка. Попробуйте позже.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Пользователь не аутентифицирован.'}, status=status.HTTP_403_FORBIDDEN)

        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema_view(
    post=extend_schema(
        summary="Вход пользователя",
        description="Позволяет пользователю войти в систему с использованием имени пользователя и пароля.",
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(
                response=None,
                description="Успешный вход."
            ),
            400: OpenApiResponse(
                response=None,
                description="Неверные учетные данные."
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Вход пользователя",
                value={
                    "username": "existinguser",
                    "password": "userpassword123",
                },
            ),
        ],
    ),
)
class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        print(f"got login request: {request.data}")
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=False)
            user = serializer.validated_data['user']

            login(request, user)

            logger.info(f"User logged in successfully: {user.username}")

            response = Response({'message': 'Успешный вход!'}, status=status.HTTP_200_OK)

            return response

        except Exception as e:
            logger.error("Login failed: Invalid credentials.")
            return Response({'error': 'Неверные учетные данные.'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        summary="Добавить продукт в избранное",
        description="Добавляет указанный продукт в избранное для текущего пользователя.",
        parameters=[
            OpenApiParameter('product_id', int, description="ID продукта для добавления в избранное", required=True),
        ],
        responses={
            201: OpenApiResponse(
                response=None,
                description="Продукт успешно добавлен в избранное."
            ),
            404: OpenApiResponse(
                response=None,
                description="Продукт не найден."
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Добавление продукта с ID 1 в избранное",
                value={
                    "product_id": 1,
                },
            ),
        ],
    ),
    get=extend_schema(
        summary="Получить избранные продукты",
        description="Возвращает список избранных продуктов текущего пользователя.",
        responses={
            200: ProductSerializer(many=True),
        },
    ),
    delete=extend_schema(
        summary="Удалить продукт из избранного",
        description="Удаляет указанный продукт из избранного для текущего пользователя.",
        parameters=[
            OpenApiParameter('product_id', int, description="ID продукта для удаления из избранного", required=True),
        ],
        responses={
            204: OpenApiResponse(
                response=None,
                description="Продукт успешно удален из избранного."
            ),
            404: OpenApiResponse(
                response=None,
                description="Продукт не найден в избранном."
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Удаление продукта с ID 1 из избранного",
                value={
                    "product_id": 1,
                },
            ),
        ],
    ),
)
class FavoritesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        profile = get_object_or_404(Profile, user=request.user)

        profile.favorite_products.add(product)

        return Response({'message': 'Продукт добавлен в избранное!'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        favorite_products = profile.favorite_products.all()

        serializer = self.get_serializer(favorite_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        profile = get_object_or_404(Profile, user=request.user)
        product = get_object_or_404(Product, id=product_id)

        if product in profile.favorite_products.all():
            profile.favorite_products.remove(product)
            return Response({'message': 'Продукт удален из избранного!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Продукт не найден в избранном!'}, status=status.HTTP_404_NOT_FOUND)