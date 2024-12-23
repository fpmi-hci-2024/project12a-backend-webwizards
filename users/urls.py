from django.urls import path

from users.views import FavoritesView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('', UserProfileAPIView.as_view(), name='user_api'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
]