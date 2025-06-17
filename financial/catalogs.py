from django.db import models


class AdjustmentIndex(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Índice")

    class Meta:
        verbose_name = "Catalogs - Índice de Reajuste"
        verbose_name_plural = "Catalogs - Índices de Reajuste"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.CharField(max_length=100, verbose_name="Produto")

    class Meta:
        verbose_name = "Catalogs - Produto"
        verbose_name_plural = "Catalogs - Produtos"

    def __str__(self):
        return self.product_type


class BillingCycle(models.Model):
    days = models.PositiveSmallIntegerField(verbose_name="Quantidade de dias")

    class Meta:
        verbose_name = "Catalogs - Ciclo de Cobrança"
        verbose_name_plural = "Catalogs - Ciclos de Cobrança"

    def __str__(self):
        return f"{self.days} dias"


class BillingCalendar(models.Model):
    cycle_date = models.DateField(verbose_name="Ciclo")

    class Meta:
        verbose_name = "Catalogs - Calendário de Faturamento"
        verbose_name_plural = "Catalogs - Calendários de Faturamento"

    def __str__(self):
        return self.cycle_date.strftime("%d/%m/%Y")


class PaymentMethod(models.Model):
    payment_type = models.CharField(max_length=100, verbose_name="Forma de Pagamento")

    class Meta:
        verbose_name = "Catalogs - Forma de Pagamento"
        verbose_name_plural = "Catalogs - Formas de Pagamento"

    def __str__(self):
        return self.payment_type
