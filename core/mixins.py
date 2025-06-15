from django.core.exceptions import ValidationError


class CleanvalidateMixin:
    """
    Mixin to provide a clean method for validating data.
    """

    def save(self, *args, **kwargs):
        if not kwargs.pop("skip_validation", False):
            self.full_clean()
        super().save(*args, **kwargs)
