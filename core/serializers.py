from django.core.validators import MinValueValidator
from rest_framework import serializers
from core.models import User, Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'amount_available', 'cost', 'product_name']


class DepositSerializer(serializers.Serializer):
    amount = serializers.ChoiceField(choices=[5, 10, 20, 50, 100])


class BuyProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField(validators=[MinValueValidator(1)])


class EmptySerializer(serializers.Serializer):
    pass

