from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import AttributeSerializer, ProductReadSerializer
from Product.models import Attribute

# where we need Attributes
# 1. Attribute list for filtering products
# 2. Attribute detail view for products with this attribute
# 3. Attribute dropdown filter for products
# 4. Attribute values for product detail view


class AttributeListView(APIView):
    """
    View to retrieve the list of attributes.
    """

    def get(self, request, *args, **kwargs):
        attributes = Attribute.objects.filter(is_active=True)
        serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AttributeDetailView(APIView):
    """
    View to retrieve the details of a specific attribute.
    """

    def get(self, request, slug):
        attribute = get_object_or_404(Attribute, slug=slug)
        serializer = AttributeSerializer(attribute)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


