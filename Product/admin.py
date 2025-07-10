from django.contrib import admin
from Product.models import (
    Category,
    ProductType,
    Tag,
    Product,
    ProductVariant,
    Attribute,
    AttributeValue,
    ProductVariantAttributeValue,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductVariantAttributeValue)