from django.urls import path

from users.views import FavoritesView, UserLoginAPIView, UserProfileAPIView, PaymentView, PaymentDetailView, \
    FavoriteDetailView

urlpatterns = [
    path('', UserProfileAPIView.as_view(), name='user_api'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('favorites/', FavoritesView.as_view(), name='favorites-list-create'),
    path('favorites/<int:product_id>/', FavoriteDetailView.as_view(), name='favorite-detail'),
    path('payments/', PaymentView.as_view(), name='payment-api'),
    path('payments/<int:payment_id>/', PaymentDetailView.as_view(), name='payment-detail'),
]
