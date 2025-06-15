from django.core.exceptions import ValidationError
from core.constraints import SLUG_PATTERN
import re


def validate_positive(value):
    """
    Validates that the given value is a positive number.

    """
    if value <= 0:
        raise ValidationError(f"value must be a positive number, got {value}.")


def validate_slug(value):
    """
    Validates that the given value is a valid slug.

    A slug consists of alphanumeric characters, underscores, or hyphens.
    """
    if len(value) > 100:
        raise ValidationError("Slug is too long (max 100 characters).")

    if " " in value:
        raise ValidationError("Slug cannot contain spaces.")

    if not re.match(SLUG_PATTERN, value):
        raise ValidationError(
            f"Slug '{value}' is not valid. It must consist of lowercase letters, numbers, underscores, or hyphens."
        )


class MinLengthValidator:
    def __init__(self, min_length):
        self.min_length = min_length

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(
                f"Value must be at least {self.min_length} characters long."
            )

    def __eq__(self, other):
        return (
            isinstance(other, MinLengthValidator)
            and self.min_length == other.min_length
        )

    def deconstruct(self):
        """
        This method tells Django how to serialize this validator into migration files.
        It returns:
        - path to the class
        - positional arguments (tuple)
        - keyword arguments (dict)
        """
        return (
            "Product.validators.MinLengthValidator",  # full python import path to this class
            (self.min_length,),  # args tuple
            {},  # kwargs dict
        )
