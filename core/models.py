from django.db import models

from django.contrib.auth.models import AbstractUser

from core.validators import validate_cost

ROLE_CHOICES = [
    ("buyer", "Buyer"),
    ("seller", "Seller"),
]


class User(AbstractUser):
    role = models.CharField(
        max_length=6, choices=ROLE_CHOICES, default="buyer"
    )
    deposit = models.IntegerField(default=0)


class Product(models.Model):
    amount_available = models.IntegerField()
    cost = models.IntegerField(validators=[validate_cost])
    product_name = models.CharField(max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
