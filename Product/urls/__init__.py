from django.urls import include, path

urlpatterns = [
    path("attributes/", include("Product.urls.Attribute_urls")),
    path("attribute-values/", include("Product.urls.attributeValues_urls")),
    path("categories/", include("Product.urls.category_urls")),
    path("product-types/", include("Product.urls.productType_urls")),
    path("products/", include("Product.urls.product_urls")),
    path("tags/", include("Product.urls.tag_urls")),
]
