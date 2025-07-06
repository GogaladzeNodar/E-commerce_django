from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import BasicProductSerializer, ProductReadSerializer, ProductWriteSerializer
from Product.models import Product

# where we need Products
# 1. Product list for filtering, sorting, and searching
# 2. Product detail view
# 3. 


class ProductListView(APIView):
    """
    View to retrieve the list of products with filtering, sorting, and searching.
    """

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_active=True)
        serializer = BasicProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    class ProductDetailView(APIView):
        """
        View to retrieve the details of a specific product.
        """

        def get(self, request, slug):
            product = get_object_or_404(Product, slug=slug, is_active=True)
            serializer = ProductReadSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

