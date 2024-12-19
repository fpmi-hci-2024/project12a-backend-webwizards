from django.urls import path

from users.views import user_favorites, register_user, add_to_favorites

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('favorites/add/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('<int:user_id>/favorites/', user_favorites, name='user_favorites'),
]