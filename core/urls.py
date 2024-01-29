from django.urls import path

from core.views import UserCreate, ProductListCreate, ProductRetrieveUpdateDestroy

urlpatterns = [
    path('users/', UserCreate.as_view(), name='user-create'),
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroy.as_view(), name='product-detail'),
]
