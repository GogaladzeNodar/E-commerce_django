from django.urls import path
from Product.views.Attribute_views import (
    AttributeListView,
    AttributeDetailView,
    AttributeWithValuesView
)


urlpatterns = [
    path('', AttributeListView.as_view(), name='attribute-list'),
    path('<slug:slug>/', AttributeDetailView.as_view(), name='attribute-detail'),
    path('<slug:slug>/values/', AttributeWithValuesView.as_view(), name='attribute-with-values'),
]
