from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    product_type = models.CharField(
        max_length=100, verbose_name="Produto", unique=True, help_text='Tipo do produto: Aéreo, Hotel, etc'
    )
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Catalogs - Produto"
        verbose_name_plural = "Catalogs - Produtos"

    def __str__(self):
        return self.product_type

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.product_type)
        return super().save(*args, **kwargs)


class BillingCycle(models.Model):
    days = models.PositiveSmallIntegerField(verbose_name="Quantidade de dias", unique=True)

    class Meta:
        verbose_name = "Catalogs - Ciclo de Cobrança"
        verbose_name_plural = "Catalogs - Ciclos de Cobrança"

    def __str__(self):
        return f"{self.days} dias"


class BillingCalendar(models.Model):
    cycle_date = models.DateField(verbose_name="Ciclo", unique=True)

    class Meta:
        verbose_name = "Catalogs - Calendário de Faturamento"
        verbose_name_plural = "Catalogs - Calendários de Faturamento"

    def __str__(self):
        return self.cycle_date.strftime("%d/%m/%Y")


class PaymentMethod(models.Model):
    payment_type = models.CharField(max_length=100, verbose_name="Forma de Pagamento", unique=True)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Catalogs - Forma de Pagamento"
        verbose_name_plural = "Catalogs - Formas de Pagamento"

    def __str__(self):
        return self.payment_type

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.payment_type)
        return super().save(*args, **kwargs)
