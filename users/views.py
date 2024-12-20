import json
import logging

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from psycopg2 import IntegrityError
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product
from shop.serializers import ProductSerializer
from users.models import Profile
from users.serializers import UserRegistrationSerializer, UserLoginSerializer

logger = logging.getLogger(__name__)

class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            # Attempt to create the user
            user = serializer.create(serializer.initial_data)
            Profile.objects.create(user=user)

            logger.info(f"User registered successfully: {user.username}")
            return Response({'message': 'Пользователь успешно зарегистрирован!'}, status=status.HTTP_201_CREATED)

        except IntegrityError:
            logger.error("User registration failed: username or email already exists.")
            return Response({'error': 'Имя пользователя или электронная почта уже заняты.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("An unexpected error occurred during user registration.")
            return Response({'error': 'Произошла ошибка. Попробуйте позже.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        serializer = self.get_serializer(favorite_products, many=True)  # Use self.get_serializer
        return Response(serializer.data, status=status.HTTP_200_OK)