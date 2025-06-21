from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from core.utils import generate_unique_slug

MODEL_CONFIGS = [
    {"app": "Product", "model": "Product"},
    {"app": "Product", "model": "Tag"},
    {"app": "Product", "model": "Category"},
    {"app": "Product", "model": "ProductType"},
    {"app": "Product", "model": "Attribute"},
]


def register_slug_signal(model_class):
    @receiver(pre_save, sender=model_class)
    def set_slug(sender, instance, **kwargs):
        if not instance.slug or (
            instance.pk
            and sender.objects.filter(pk=instance.pk).exists()
            and sender.objects.get(pk=instance.pk).name != instance.name
        ):
            generate_unique_slug(instance, sender, field_name="name", slug_field="slug")


for config in MODEL_CONFIGS:
    model_class = apps.get_model(config["app"], config["model"])
    register_slug_signal(model_class)
