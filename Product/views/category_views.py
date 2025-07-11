from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Product.serializers import CategorySerializer, CategoryBasicSerializer
from Product.models import Category


# where we need Categories?
# 1. menu - categories with nested subcategories
# 2. dropdown filter - categories with subcategories
# 3. Breadcrumbs - Home > Electronics > Phones > Android


class CategoryTreeView(APIView):
    """
    View to retrieve the category tree with nested subcategories.
    """

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent=None, is_active=True)
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDropdownView(APIView):
    """
    View to retrieve categories with their subcategories for dropdown filters.
    """

    def get(self, request):
        categories = Category.objects.filter(parent=None, is_active=True)
        serializer = CategoryBasicSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Breadcrumbs - for this view we need serializer (only id, name, slug)


class CategoryDetailView(APIView):
    """
    Returns full detail of a category including children.
    """

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
