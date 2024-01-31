from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from core.models import Product
from core.serializers import UserSerializer, ProductSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
