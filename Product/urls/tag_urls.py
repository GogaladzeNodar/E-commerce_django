from django.urls import path
from Product.views.Tag_views import TagListView, TagDetailView, ProductsByTagView

urlpatterns = [
    path('', TagListView.as_view(), name='tag-list'),
    path('<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),
    path('<slug:slug>/products/', ProductsByTagView.as_view(), name='products-by-tag'),
]
