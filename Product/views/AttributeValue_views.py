from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import AttributeValueSerializer
from Product.models import AttributeValue




