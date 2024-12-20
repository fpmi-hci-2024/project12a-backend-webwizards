from django.urls import path

from users.views import FavoritesView, UserRegistrationAPIView, UserLoginAPIView

urlpatterns = [
    path('', UserRegistrationAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
]