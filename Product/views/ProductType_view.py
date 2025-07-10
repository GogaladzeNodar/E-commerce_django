from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import ProductTypeSerializer
from Product.models import ProductType

# where we need Product Types
# Main ProductType list
# ProductType detail 
# ProductType dropdown filter

class ProductTypeListView(APIView):
    """
    View to retrieve the list of product types.
    """

    def get(self, request, *args, **kwargs):
        product_types = ProductType.objects.filter(is_active=True)
        serializer = ProductTypeSerializer(product_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductTypeDetailView(APIView):
    """
    View to retrieve the details of a specific product type.
    """

    def get(self, request, slug):
        product_type = get_object_or_404(ProductType, slug=slug)
        serializer = ProductTypeSerializer(product_type)
        return Response(serializer.data, status=status.HTTP_200_OK)




