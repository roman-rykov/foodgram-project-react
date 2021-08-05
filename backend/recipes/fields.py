import base64
import binascii
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import fields
from rest_framework.exceptions import ValidationError


class Base64ImageField(fields.ImageField):

    def to_internal_value(self, data):
        try:
            format, encoded_str = data.split(';base64,')
            decoded = base64.b64decode(encoded_str)
            extension = format.split('/')[-1]
        except (AttributeError, ValueError, binascii.Error):
            raise ValidationError
        filename = str(uuid.uuid4()) + '.' + extension
        image_file = SimpleUploadedFile(name=filename, content=decoded)
        return super().to_internal_value(image_file)
