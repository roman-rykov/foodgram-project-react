from rest_framework.exceptions import ValidationError


class UniqueValuesValidator:
    message = (
        'Each of these fields ({field_names}) must contain a unique'
        ' value.'
    )

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or self.message

    def __call__(self, attrs):
        values = [attrs[field] for field in self.fields]
        if len(values) > len(set(values)):
            message = self.message.format(field_names=', '.join(self.fields))
            raise ValidationError(message)
