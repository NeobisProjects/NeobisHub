from django.core.validators import RegexValidator

number = r"^[+996][0-9]{12,12}$"


def validate_number():
    return [RegexValidator(regex=number, message='Number in format: +996555111222')]
