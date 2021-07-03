from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='наименование',
        max_length=32,
    )
    color = models.CharField(
        verbose_name='цвет',
        max_length=7,
        default='#FFFFFF',
        validators=[RegexValidator('^#(?:[0-9a-fA-F]{1,2}){3}$')])
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name
