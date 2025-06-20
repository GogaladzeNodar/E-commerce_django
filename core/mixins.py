from django.core.exceptions import ValidationError


class CleanvalidateMixin:
    """
    Mixin to provide a clean method for validating data.
    """

    def save(self, *args, **kwargs):
        if not kwargs.pop("skip_validation", False):
            self.full_clean()
        super().save(*args, **kwargs)


class PreventDeactivationIfUsedMixin:
    """
    Prevents deactivation of an object if it's referenced by other models.
    """

    @classmethod
    def get_related_check(cls):
        """
        Returns list of (related_model, foreign_key_field_name) pairs.
        Override in subclasses.
        """
        return []

    def clean(self):
        super_clean = getattr(super(), "clean", None)
        if callable(super_clean):
            super_clean()

        if self.pk and getattr(self, "is_active", True) is False:
            for model_class, related_field in self.get_related_check():
                filter_kwargs = {related_field: self}
                if model_class.objects.filter(**filter_kwargs).exists():
                    raise ValidationError(
                        f"Can't deactivate this object. {model_class.__name__} objects are using it."
                    )
