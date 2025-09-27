from django.db import models
from django.core.exceptions import ValidationError

def validate_nombre_corto(value):
    if not value.isupper():
        raise ValidationError('El nombre corto debe ser todo en mayúsculas.')

class Oficina(models.Model):
    """Model definition for Oficina."""

    nombre = models.CharField(verbose_name="Nombre de la oficina", max_length=50, unique=True)
    nombre_corto = models.SlugField(
        verbose_name="Id Corto",
        max_length=10,
        unique=True,
        help_text="Código corto único (ej: PER, ADM, etc.)",
        validators=[validate_nombre_corto]
    )

    class Meta:
        """Meta definition for Oficina."""

        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'

    def __str__(self):
        """Unicode representation of Oficina."""
        return f"{self.nombre} ({self.nombre_corto})"

