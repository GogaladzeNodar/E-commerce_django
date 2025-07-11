from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import AttributeValueSerializer
from Product.models import AttributeValue

# at first, what we need here
# listwiew
# attributeview

class AttributeValueListView(APIView):
    """
    List all attribute values or create a new attribute value.
    """
    def get(self, request):
        attribute_values = AttributeValue.objects.all()
        serializer = AttributeValueSerializer(attribute_values, many=True)
        return Response(serializer.data)



class AttributeValueDetailView(APIView):
    """
    Retrieve a specific attribute value by its slug.
    """
    def get_object(self, slug):
        return get_object_or_404(AttributeValue, slug=slug)

    def get(self, request, slug):
        attribute_value = self.get_object(slug)
        serializer = AttributeValueSerializer(attribute_value)
        return Response(serializer.data)



