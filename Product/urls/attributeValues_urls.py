from django.urls import path
from Product.views.AttributeValue_views import (
    AttributeValueListView,
    AttributeValueDetailView,
)

urlpatterns = [
    path('', AttributeValueListView.as_view(), name='attribute-value-list'),
    path('<slug:slug>/', AttributeValueDetailView.as_view(), name='attribute-value-detail'),
]


