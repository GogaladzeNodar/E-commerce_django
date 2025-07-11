from django.urls import path
from Product.views.ProductType_views import ProductTypeListView, ProductTypeDetailView

urlpatterns = [
    path('', ProductTypeListView.as_view(), name='product-type-list'),
    path('<slug:slug>/', ProductTypeDetailView.as_view(), name='product-type-detail'),
]