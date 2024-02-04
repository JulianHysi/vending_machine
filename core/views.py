from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import status

from core.models import Product
from core.permissions import IsSellerOrReadOnly
from core.serializers import UserSerializer, ProductSerializer, DepositSerializer, BuyProductSerializer
from core.utils import get_change_in_fewest_coins

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'deposit':
            return DepositSerializer
        elif self.action == 'buy':
            return BuyProductSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # no auth; anyone can sign up
        return super().get_permissions()

    @action(methods=["POST"], detail=False)
    def deposit(self, request):
        user = request.user
        serializer = DepositSerializer(data=request.data)

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

    @action(methods=["POST"], detail=False)
    def buy(self, request):
        user = request.user
        serializer = BuyProductSerializer(data=request.data)

        if user.role != "buyer":
            return Response(
                {'detail': 'Only buyers can buy.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            product = serializer.validated_data['product']
            amount = serializer.validated_data['amount']
            purchase_total = product.cost * amount
            change = user.deposit - purchase_total
            if change < 0:
                return Response(
                    {'detail': 'Not enough money.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user.deposit -= purchase_total
                user.save()
                product.amount_available -= amount
                product.save()

            return Response(
                {
                    'purchase_total': purchase_total,
                    'product': product.product_name,
                    'change': get_change_in_fewest_coins(change),
                },
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
