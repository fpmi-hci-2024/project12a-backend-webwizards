# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from cart.models import Cart
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        Cart.objects.create(profile=profile)