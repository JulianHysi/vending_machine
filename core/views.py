from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import status

from core.models import Product
from core.permissions import IsSellerOrReadOnly
from core.serializers import UserSerializer, ProductSerializer, DepositSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'deposit':
            return DepositSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # no auth; anyone can sign up
        return super().get_permissions()

    @action(methods=["POST"], detail=True)
    def deposit(self, request, pk=None):
        user = self.get_object()
        serializer = DepositSerializer(data=request.data)

        if request.user != user:
            return Response(
                {'detail': 'Cannot deposit to another account.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if user.role != "buyer":
            return Response(
                {'detail': 'Only buyers can deposit.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user.deposit += amount
            user.save()
            return Response(
                {'status': 'deposit added', 'new deposit': user.deposit},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
