from django.db import models
from companies.models import CompanyRelatedModel


class ContractData(CompanyRelatedModel):
    signature_date = models.DateField(verbose_name="Data de Assinatura")
    expiration_date = models.DateField(verbose_name="Data de Expiração")
    adjustment_date = models.DateField(verbose_name="Data de Reajuste")
    adjustment_index = models.ForeignKey(
        "AdjustmentIndex", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Índices para Reajuste"
    )

    class Meta:
        verbose_name = "Dados Contratuais"
        verbose_name_plural = "Dados Contratuais"

    def __str__(self):
        return f'{self.company} - Signature Date: {self.signature_date.strftime('%Y-%m-%d')}'


class BillingPolicy(CompanyRelatedModel):
    products_to_bill = models.ManyToManyField("Product", verbose_name="Produtos a Faturar")
    cycle = models.ForeignKey("BillingCycle", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ciclo")
    term_days = models.PositiveSmallIntegerField(verbose_name="Prazo")
    calendar = models.ForeignKey(
        "BillingCalendar", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Calendário"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Política de Faturamento"
        verbose_name_plural = "Políticas de Faturamento"

    def __str__(self):
        return f'{self.company} - Cycle: {self.cycle.days} days'


class InvoiceCreationChoices(models.TextChoices):
    BY_CLIENT = "BY_CLIENT", "Por Cliente"
    BY_GROUP = "BY_GROUP", "Por Grupo"


class InvoiceConfig(CompanyRelatedModel):
    creation_type = models.CharField(
        max_length=20, choices=InvoiceCreationChoices.choices, verbose_name="Criação da Fatura"
    )
    has_cutoff = models.BooleanField(verbose_name="Possui data de corte?")
    cutoff_days = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Dias de corte")
    payment_methods = models.ManyToManyField("PaymentMethod", verbose_name="Forma de Pagamento")

    class Meta:
        verbose_name = "Configuração de Fatura"
        verbose_name_plural = "Configurações de Fatura"

    def __str__(self):
        return f'{self.company} - Creation Type: {self.creation_type}'


class FinancialContact(CompanyRelatedModel):
    name = models.CharField(max_length=100, verbose_name="Nome")
    role = models.CharField(max_length=100, verbose_name="Cargo")
    phone = models.CharField(max_length=30, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    is_billing_contact = models.BooleanField(default=False, verbose_name="Contato para Cobrança")

    class Meta:
        verbose_name = "Contato Financeiro"
        verbose_name_plural = "Contatos Financeiros"

    def __str__(self):
        return f"{self.name} - {self.role}"


class FeeDispatchContact(FinancialContact):
    invoice_to = models.CharField(max_length=100, verbose_name="Emitir NF para")

    class Meta:
        verbose_name = "Contato para Envio do FEE"
        verbose_name_plural = "Contatos para Envio do FEE"

    def __str__(self):
        return f'{self.company} - Invoice To: {self.invoice_to}'


class FeeBilling(CompanyRelatedModel):
    products_to_charge = models.ManyToManyField("Product", verbose_name="Quais produtos cobrar o FEE")
    charge_type = models.CharField(max_length=100, verbose_name="Tipo de cobrança")

    class Meta:
        verbose_name = "Faturamento FEE"
        verbose_name_plural = "Faturamentos FEE"

    def __str__(self):
        return f'{self.company} - Charge Type: {self.charge_type}'


class FeeDetails(CompanyRelatedModel):
    cycle = models.ForeignKey("BillingCycle", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ciclo")
    send_report = models.BooleanField(verbose_name="Enviar Relatório")
    term_date = models.DateField(verbose_name="Prazo")
    fee_closing_date = models.DateField(verbose_name="Fechamento do FEE")
    fee_report = models.BooleanField(verbose_name="Relatório do FEE")
    fee_invoice = models.BooleanField(verbose_name="Fatura do FEE")
    validation = models.CharField(max_length=50, verbose_name="Validação")
    payment_method = models.ForeignKey(
        "PaymentMethod", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Forma de Pagamento"
    )
    cutoff_date = models.DateField(verbose_name="Data de Corte")
    dispatch_date = models.DateField(verbose_name="Data de Envio")
    payment_date = models.DateField(verbose_name="Dia do Pagamento")
    has_invoice_report = models.BooleanField(verbose_name="NF do Relatório")
    cancelation_fee = models.BooleanField(verbose_name="Cobrar taxa de cancelamento")
    include_du_fee = models.BooleanField(verbose_name="Incluir Taxa DU")

    class Meta:
        verbose_name = "Detalhes do FEE"
        verbose_name_plural = "Detalhes do FEE"

    def __str__(self):
        return f"{self.company} - {self.fee_closing_date.strftime('%Y-%m-%d')}"
