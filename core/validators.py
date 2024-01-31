from django.core.exceptions import ValidationError


def validate_cost(value):
    if value <= 0:
        raise ValidationError('Cost cannot be less than or equal to 0!')
    if value % 5 != 0:
        raise ValidationError('Cost has to be a multiple of 5!')
