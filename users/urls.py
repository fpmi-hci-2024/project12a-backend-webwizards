from django.urls import path

from users.views import register_user, FavoritesView

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
]