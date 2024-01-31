from django.db import models

from django.contrib.auth.models import AbstractUser

from core.validators import validate_cost


class User(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default=BUYER)
    deposit = models.IntegerField(default=0)


class Product(models.Model):
    amount_available = models.IntegerField()
    cost = models.IntegerField(validators=[validate_cost])
    product_name = models.CharField(max_length=255)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
