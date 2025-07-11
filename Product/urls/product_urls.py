from django.urls import path
from Product.views.Product_views import (
    ProductListView,
    ProductDetailView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]