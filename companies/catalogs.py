from django.db import models
from django.utils.text import slugify


class PointOfSale(models.Model):
    name = models.CharField('Ponto de Venda', max_length=255, help_text='Ponto de venda')
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Catalogs - Ponto de Venda"
        verbose_name_plural = "Catalogs - Pontos de Venda"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
