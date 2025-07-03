from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from core.utils import generate_unique_slug

MODEL_CONFIGS = [
    {"app": "Product", "model": "Product", "field": "name"},
    {"app": "Product", "model": "Tag", "field": "name"},
    {"app": "Product", "model": "Category", "field": "name"},
    {"app": "Product", "model": "ProductType", "field": "name"},
    {"app": "Product", "model": "Attribute", "field": "name"},
    {"app": "Product", "model": "AttributeValue", "field": "value"},
]


def register_slug_signal(model_class, field_name):
    @receiver(pre_save, sender=model_class)
    def set_slug(sender, instance, **kwargs):
        if not instance.slug or (
            instance.pk
            and sender.objects.filter(pk=instance.pk).exists()
            and getattr(sender.objects.get(pk=instance.pk), field_name)
            != getattr(instance, field_name)
        ):
            generate_unique_slug(
                instance, sender, field_name=field_name, slug_field="slug"
            )


for config in MODEL_CONFIGS:
    model_class = apps.get_model(config["app"], config["model"])
    field_name = config.get("field", "name")
    register_slug_signal(model_class, field_name)
