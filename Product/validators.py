from django.core.exceptions import ValidationError
from core.constraints import SLUG_PATTERN
import re

def validate_positive(value):
    """
    Validates that the given value is a positive number.
    
    """
    if value <= 0:
        raise ValidationError(
            f"value must be a positive number, got {value}."
        )
    


def validate_slug(value):
    """
    Validates that the given value is a valid slug.
    
    A slug consists of alphanumeric characters, underscores, or hyphens.
    """
    if len(value) > 100:
        raise ValidationError("Slug is too long (max 100 characters).")
    
    if ' ' in value:
        raise ValidationError("Slug cannot contain spaces.")
    
    if not re.match(SLUG_PATTERN, value):
        raise ValidationError(
            f"Slug '{value}' is not valid. It must consist of lowercase letters, numbers, underscores, or hyphens."
        )