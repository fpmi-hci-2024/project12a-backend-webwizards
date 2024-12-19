import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from shop.models import Product
from users.models import Profile


@csrf_exempt
def register_user(self, request):
    try:
        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Имя пользователя уже занято.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Электронная почта уже используется.'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'message': 'Пользователь успешно зарегистрирован!'}, status=201)

    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': 'Некорректный JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@login_required
def add_to_favorites(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        profile = get_object_or_404(Profile, user=request.user)

        profile.favorite_products.add(product)

        return JsonResponse({'message': 'Продукт добавлен в избранное!'}, status=201)

    return JsonResponse({'error': 'Метод не разрешен.'}, status=405)

def user_favorites(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    favorite_products = profile.favorite_products.all()

    favorite_product_names = [product.name for product in favorite_products]
    return JsonResponse(favorite_product_names, safe=False)