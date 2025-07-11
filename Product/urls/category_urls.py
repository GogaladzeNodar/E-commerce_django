from django.urls import path
from Product.views.category_views import CategoryTreeView, CategoryDropdownView, CategoryDetailView

urlpatterns = [
    path('tree/', CategoryTreeView.as_view(), name='category-tree'),
    path('dropdown/', CategoryDropdownView.as_view(), name='category-dropdown'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
]