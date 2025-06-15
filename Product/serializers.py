from rest_framework import serializers
from .models import Product, Category, ProductType
import re
from core import validators

from core.constraints import SLUG_PATTERN

###################################
# category Serializers
###################################


class BaseCategorySerializer(serializers.ModelSerializer):
    """
    Base serializer for Category model.
    Provides basic fields and validation.
    """

    name = serializers.CharField(validators=[validators.MinLengthValidator(3)])
    slug = serializers.SlugField(validators=[validators.validate_slug])

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "is_active",
            "parent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_is_active(self, value):
        """
        Validates that the category can only be deactivated if it has no active children.
        """
        if self.instance and not value:
            if self.instance.get_children().filter(is_active=True).exists():
                raise serializers.ValidationError(
                    "Cannot deactivate category with active children."
                )
        return value

    def validate(self, attrs):
        """
        Validates that the category does not become its own parent,
        and that the slug is unique within the same parent category.
        """
        parent = attrs.get("parent")
        instance = self.instance

        if instance and parent and parent == instance:
            raise serializers.ValidationError("Category cannot be its own parent.")

        if instance and parent:
            if parent in instance.get_descendants():
                raise serializers.ValidationError(
                    "Category cannot be a child of its own descendant."
                )

        slug = attrs.get("slug")
        if (
            slug
            and Category.objects.filter(slug=slug, parent=parent)
            .exclude(pk=getattr(instance, "pk", None))
            .exists()
        ):
            raise serializers.ValidationError(
                {"slug": "Slug must be unique within the same parent category."}
            )

        return attrs


class CategorySerializer(BaseCategorySerializer):
    """
    Serializer for Category Tree.
    """

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = BaseCategorySerializer.Meta.fields + ["children"]

    def get_children(self, obj):
        """
        full nested view of children categories.
        """
        children = obj.get_children.all()
        serializer = CategorySerializer(children, many=True)
        return serializer.data


class CategoryBasicSerializer(BaseCategorySerializer):
    """
    Basic serializer for Category model.
    Provides only essential fields without children.
    """

    class Meta:
        model = Category
        fields = BaseCategorySerializer.Meta.fields


###################################
# ProductType Serializers
###################################


class ProductTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductType model.
    """

    name = serializers.CharField(validators=[validators.MinLengthValidator(3)])
    slug = serializers.SlugField(validators=[validators.validate_slug])

    class Meta:
        model = ProductType
        fields = ["id", "name", "slug", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
