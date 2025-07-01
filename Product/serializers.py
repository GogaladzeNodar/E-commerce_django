from rest_framework import serializers
from .models import (
    Product,
    Category,
    ProductType,
    Tag,
    ProductVariantAttributeValue,
    AttributeValue,
    Attribute,
)
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
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

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
        model = BaseCategorySerializer.Meta.model
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
        model = BaseCategorySerializer.Meta.model
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
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, attrs):
        """
        IF there is an active product parent product can't be deactivated.
        IF there is an active product parent product can't be deleted.
        """
        is_active = attrs.get("is_active", True)
        instance = self.instance

        if instance and instance.is_active and not is_active:
            has_active_products = Product.objects.filter(
                product_type=instance, is_active=True
            ).exists()
            if has_active_products:
                raise serializers.ValidationError(
                    "Cannot deactivate ProductType with active products."
                )


###############################
# Tag Serializers
###############################


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """

    name = serializers.CharField(validators=[validators.MinLengthValidator(3)])
    slug = serializers.SlugField(validators=[validators.validate_slug])

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, attrs):
        """
        and that the slug is unique.
        """

        slug = attrs.get("slug")
        if (
            slug
            and Tag.objects.filter(slug=slug)
            .exclude(pk=getattr(self.instance, "pk", None))
            .exists()
        ):
            raise serializers.ValidationError(
                {"slug": "Slug must be unique within the same parent category."}
            )
        return attrs


#################################
# Product Serializers
#################################


class BasicProductSerializer(serializers.Serializer):
    """
    Basic serializer for Product model.
    """

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[validators.MinLengthValidator(3)])
    slug = serializers.SlugField(read_only=True, validators=[validators.validate_slug])
    description = serializers.CharField(allow_blank=True, required=False, default="")
    image = serializers.ImageField(allow_null=True, required=False, default=None)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class ProductReadSerializer(BasicProductSerializer):
    """
    Read serializer for Product model.
    Provides detailed information about the product.
    """

    categories = CategoryBasicSerializer(many=True, read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class ProductWriteSerializer(BasicProductSerializer):
    """
    Write serializer for Product model.
    Used for creating and updating products.
    """

    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    product_type = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all(), allow_null=True, required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), allow_null=True, required=False
    )

    def create(self, validated_data):
        """
        Create a new product instance.
        """
        categories = validated_data.pop("categories", [])
        tags = validated_data.pop("tags", [])
        product_type = validated_data.pop("product_type", None)

        product = Product.objects.create(**validated_data, product_type=product_type)
        product.categories.set(categories)
        product.tags.set(tags)
        return product

    def update(self, instance, validated_data):
        """
        Update an existing product instance.
        """
        categories = validated_data.pop("categories", None)
        tags = validated_data.pop("tags", None)
        product_type = validated_data.pop("product_type", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if product_type is not None:
            instance.product_type = product_type
        if categories is not None:
            instance.categories.set(categories)
        if tags is not None:
            instance.tags.set(tags)
        instance.save()


################################
# attribute Serializers
################################


class AttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for Attribute model.
    """

    name = serializers.CharField(validators=[validators.MinLengthValidator(3)])
    slug = serializers.SlugField(validators=[validators.validate_slug])

    class Meta:
        model = Attribute
        fields = ["id", "name", "slug", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


################################
# AttributeValue Serializer
################################


class AttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer for AttributeValue model.
    """

    class Meta:
        model = AttributeValue
        fields = [
            "id",
            "attribute",
            "value",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


#################################
# Productvariant Serializers
#################################


class ProductVariantSerializer(serializers.Serializer):
    """
    Serializer for ProductVariant model.
    """

    id = serializers.ReadOnlyField()
    sku = serializers.CharField(max_length=100)
    price = serializers.DecimalField()
    stock = serializers.IntegerField()
    image = serializers.ImageField(allow_null=True, required=False)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)

    attributes = serializers.SerializerMethodField()

    def get_attributes(self, obj):
        return [
            {"attribute": item.attribute.name, "value": item.attribute_value.value}
            for item in obj.attribute_values.all()
        ]


class ProductVariantAttributeValueSerializer(serializers.modelserialaizer):
    """
    ProductVariantAttributeValue serializer
    """

    class Meta:
        model = ProductVariantAttributeValue
        fields = [
            "id",
            "product_variant",
            "attribute_value",
            "attribute",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
