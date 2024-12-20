from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

# Create your views here.
class CartAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_cart(self):
        return Cart.objects.get(profile=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        cart = self.get_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        item_serializer = CartItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save(cart=cart)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart = self.get_cart()
        cart.items.all().delete()  # Clear all items in the cart
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_cart(self):
        return Cart.objects.get(profile=self.request.user.profile)

    def get_cart_item(self, pk):
        cart = self.get_cart()
        return cart.items.get(id=pk)

    def delete(self, request, *args, **kwargs):
        try:
            cart_item = self.get_cart_item(kwargs['pk'])
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Элемент не найден."}, status=status.HTTP_404_NOT_FOUND)