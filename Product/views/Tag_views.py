from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import TagSerializer, ProductReadSerializer
from Product.models import Tag

# where we need Tags
# 1. Tag list for filtering products
# 2. Tag detail view for products with this tag
# 3. Tag dropdown filter for products


class TagListView(APIView):
    """
    View to retrieve the list of tags.
    """

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.filter(is_active=True)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class TagDetailView(APIView):
    """
    View to retrieve the details of a specific tag.
    """

    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsByTagView(APIView):
    """
    View to retrieve products associated with a specific tag.
    """

    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug=slug, is_active=True)
        products = tag.products.filter(is_active=True)
        serializer = ProductReadSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

        
