from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from Product import validators
from core.mixins import CleanvalidateMixin


class Category(MPTTModel, CleanvalidateMixin):
    """
    Category table implimented with MPTT
    """

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Category Name",
        validators=[validators.MinLengthValidator(3)],
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
        verbose_name="Category Slug",
        validators=[validators.validate_slug],
    )
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent Category",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class MPTTMeta:
        order_insertion_by = ["name"]
        level_attr = "mptt_level"
        parent_attr = "parent"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class ProductType(CleanvalidateMixin, models.Model):
    """
    Product Type table
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Product Type Name",
        validators=[validators.MinLengthValidator(3)],
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="Product Type Slug",
        validators=[validators.validate_slug],
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(CleanvalidateMixin, models.Model):
    """
    Tag table
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Tag Name",
        validators=[validators.MinLengthValidator(3)],
    )
    slug = models.SlugField(
        max_length=60, unique=True, validators=[validators.validate_slug]
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return f"#{self.name}"


class Product(CleanvalidateMixin, models.Model):
    """
    Product table
    """

    name = models.CharField(
        max_length=100,
        unique=False,
        null=False,
        blank=False,
        verbose_name="Product Name",
        validators=[validators.MinLengthValidator(3)],
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Product Slug",
        validators=[validators.validate_slug],
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Product Description"
    )
    categories = TreeManyToManyField(
        Category, related_name="products", verbose_name="Product Category"
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Product Type",
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    image = models.ImageField(
        upload_to="product_images/", null=True, blank=True, verbose_name="Product Image"
    )
    is_active = models.BooleanField(
        default=True, unique=False, null=False, blank=False, verbose_name="Is Active"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        errors = {}

        if self.product_type is None:
            errors["product_type"] = "Product type is required."

        if (
            self.pk
            and not self.is_active
            and self.variants.filter(is_active=True).exists()
        ):
            errors["is_active"] = (
                "Cannot deactivate a product that has active variants."
            )

        if errors:
            raise ValidationError(errors)


class Attribute(CleanvalidateMixin, models.Model):
    """
    Attribute table
    """

    product_types = models.ManyToManyField(
        "ProductType",
        related_name="attributes",
        blank=True,
        verbose_name="Product Types",
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Attribute Name",
        validators=[validators.MinLengthValidator(3)],
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Attribute Slug",
        validators=[validators.validate_slug],
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Attribute Description"
    )
    is_filterable = models.BooleanField(default=False, verbose_name="Is Filterable")
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"
        ordering = ["name"]


class AttributeValue(CleanvalidateMixin, models.Model):
    """
    AttributeValue
    """

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
        verbose_name="Attribute",
    )
    value = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Attribute Value"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Attribute Value Slug",
        validators=[validators.validate_slug],
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        ordering = ["value"]
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(CleanvalidateMixin, models.Model):
    """
    ProductVariant table
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Product",
    )
    sku = models.CharField(
        max_length=100, unique=True, null=False, blank=False, verbose_name="SKU"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name="Price",
        validators=[validators.validate_positive],
    )

    stock = models.IntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name="Stock",
        validators=[validators.validate_positive],
    )
    image = models.ImageField(upload_to="variant_images/", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ["product", "sku"]

    def __str__(self):
        return f"{self.product.name if self.product else 'Unknown'} - {self.sku}"


class ProductVariantAttributeValue(CleanvalidateMixin, models.Model):
    """
    ProductVariantAttributeValue table
    """

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attribute_values",
        verbose_name="Product Variant",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="variant_attributes",
        verbose_name="Attribute",
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="variant_values",
        verbose_name="Attribute Value",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product Variant Attribute Value"
        verbose_name_plural = "Product Variant Attribute Values"
        constraints = [
            models.UniqueConstraint(
                fields=["variant", "attribute"], name="unique_variant_attribute"
            )
        ]

    def __str__(self):
        return (
            f"{self.variant.sku} - {self.attribute.name}: {self.attribute_value.value}"
        )

    def clean(self):
        super().clean()

        errors = {}

        product = getattr(self.variant, "product", None)
        product_type = getattr(product, "product_type", None)

        attribute = self.attribute
        attribute_value = self.attribute_value

        if not product_type:
            errors["variant"] = ValidationError(
                "Cannot validate because product type is missing.",
                code="missing_product_type",
            )
            raise ValidationError(errors)

        if product_type not in attribute.product_types.all():
            errors["attribute"] = ValidationError(
                f"Attribute '{attribute.name}' is not valid for product type '{product_type.name}'.",
                code="invalid_product_type",
            )

        if attribute_value.attribute != attribute:
            errors["attribute_value"] = ValidationError(
                "Selected attribute value does not belong to the given attribute.",
                code="invalid_attribute_value",
            )

        if errors:
            raise ValidationError(errors)
