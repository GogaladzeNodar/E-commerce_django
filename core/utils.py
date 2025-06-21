from django.utils.text import slugify


def generate_unique_slug(
    instance, model, field_name="name", slug_field="slug", slugify_func=slugify
):
    """
    Generate a unique slug for a given model instance.
    """
    base_value = getattr(instance, field_name, None)
    if not base_value:
        raise ValueError(f"Cannot generate slug: '{field_name}' is empty.")

    base_slug = slugify_func(base_value)
    slug = base_slug
    counter = 1

    qs = model.objects.exclude(pk=instance.pk) if instance.pk else model.objects.all()

    while qs.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    setattr(instance, slug_field, slug)
