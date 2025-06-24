from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from companies.catalogs import PointOfSale
from shared.models import TimeStampedModel


class CompanyRelatedModel(TimeStampedModel):
    company = models.ForeignKey(
        "companies.Company",  # app_label.ModelName
        on_delete=models.CASCADE,
        verbose_name="Empresa",
        related_name="%(class)s"
    )

    class Meta:
        abstract = True


class CompanyGroup(models.Model):
    name = models.CharField("Nome do Grupo", max_length=255)
    slug = models.SlugField("Slug", unique=True)
    main_company = models.OneToOneField(
        "Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="is_main_company_of",
        verbose_name="Empresa Principal",
        help_text="Empresa principal do grupo"
    )

    def clean(self):
        super().clean()
        if self.main_company and self.main_company.group_id != self.id:
            raise ValidationError({
                'main_company': "A empresa principal deve pertencer a este grupo."
            })

    class Meta:
        verbose_name = "Grupo da Empresa"
        verbose_name_plural = "Grupos das Empresas"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()
        return super().save(*args, **kwargs)


class Company(models.Model):
    group = models.ForeignKey(
        "CompanyGroup", on_delete=models.PROTECT, related_name="companies", verbose_name="Grupo",
        help_text="Grupo ao qual esta empresa pertence"
    )
    go_live = models.DateField(verbose_name="Go Live")
    name = models.CharField('Razão Social', max_length=255, help_text='Nome jurídico oficial', unique=True)
    fantasy_name = models.CharField(
        'Nome Fantasia', max_length=255, help_text='Nome utilizado comercialmente', unique=True
    )
    cnpj = models.CharField('CNPJ', max_length=14, help_text='Validação obrigatória', unique=True)
    full_address = models.TextField(
        'Endereço Completo', blank=True, null=True, help_text='Utilizado para referência e notas fiscais'
    )
    point_of_sale = models.ForeignKey(
        PointOfSale, on_delete=models.PROTECT, related_name="point", verbose_name="Ponto de Venda"
    )
    segment = models.CharField('Segmento', max_length=255, help_text='Ex: Saúde, Educação, Indústria')
    benner_code = models.CharField(
        'Código Interno (Benner)', max_length=255, help_text='Código cadastrado no sistema Benner'
    )
    obt_link = models.CharField('Link do OBT', max_length=255, help_text='Endereço da Argo ou outro OBT')
    website = models.CharField('Site', max_length=255, blank=True, null=True, help_text='Página institucional')
    notes = models.TextField(
        'Observações/Particularidades', blank=True, null=True, help_text='Regras específicas por cliente'
    )

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.cnpj:
            cnpj_numeric = self.cnpj.replace('.', '').replace('/', '').replace('-', '')
            if len(cnpj_numeric) != 14 or not cnpj_numeric.isdigit():
                raise ValidationError({'cnpj': 'CNPJ inválido.'})
            self.cnpj = cnpj_numeric

    @property
    def cnpj_formatted(self):
        if self.cnpj and len(self.cnpj) == 14:
            return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}"
        return self.cnpj

    @property
    def travel_managers(self):
        return self.companycontact.filter(is_travel_manager=True)

    @property
    def account_executives(self):
        return self.companycontact.filter(is_account_executive=True)

    @property
    def billing_contacts(self):
        return self.companycontact.filter(is_billing_contact=True)

    @property
    def vip(self):
        return self.vip.all()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CompanyContact(CompanyRelatedModel):
    name = models.CharField(max_length=100, verbose_name="Nome", unique=True)
    role = models.CharField(max_length=100, verbose_name="Cargo")
    phone = models.CharField(max_length=30, verbose_name="Telefone Fixo", blank=True)
    mobile = models.CharField(max_length=30, verbose_name="Celular", blank=True)
    whatsapp = models.CharField(max_length=30, verbose_name="WhatsApp", blank=True)
    email = models.EmailField(verbose_name="E-mail", unique=True)
    is_travel_manager = models.BooleanField(default=False, verbose_name="Gestor de Viagem")
    is_account_executive = models.BooleanField(default=False, verbose_name="Executivo de Contas")
    is_billing_contact = models.BooleanField(default=False, verbose_name="Contato para Cobrança")

    class Meta:
        verbose_name = "Contato da Empresa"
        verbose_name_plural = "Contatos das Empresas"

    def __str__(self):
        return f'{self.company} - Contact: {self.name}'

    def clean(self):
        self._clean_phone_field("phone", expected_length=10, label="Telefone fixo")
        self._clean_phone_field("mobile", expected_length=11, label="Telefone móvel")
        self._clean_phone_field("whatsapp", expected_length=11, label="WhatsApp")

    def _clean_phone_field(self, field_name, expected_length, label):
        value = getattr(self, field_name)
        if value:
            numeric = value.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
            if len(numeric) != expected_length or not numeric.isdigit():
                raise ValidationError({
                    field_name: f"{label} precisa conter {expected_length} dígitos: DDD e número do telefone"
                })
            setattr(self, field_name, numeric)

    def save(self, *args, **kwargs):
        self.full_clean()  # Chama o clean acima, e os campos já serão formatados
        super().save(*args, **kwargs)


class FeeDispatchContact(CompanyRelatedModel):
    invoice_to = models.ForeignKey(
        "CompanyContact", on_delete=models.PROTECT, related_name="fee_dispatches", verbose_name="Emitir NF para",
        help_text="Deve ser um Contato para Cobrança. Cadastre um usuário com este perfil em Contato da Empresa"
    )

    class Meta:
        verbose_name = "Contato para Envio do FEE"
        verbose_name_plural = "Contatos para Envio do FEE"

    def __str__(self):
        return f'{self.company} - Invoice To: {self.invoice_to}'

    def clean(self):
        super().clean()
        if not self.invoice_to.is_billing_contact:
            raise ValidationError({"invoice_to": "O contato escolhido não é marcado como 'Contato para Cobrança'."})


class Vip(models.Model):
    company_contact = models.ForeignKey(
        "CompanyContact",
        on_delete=models.CASCADE,
        related_name="vips",
        verbose_name="Contato"
    )
    is_requester = models.BooleanField(default=False, verbose_name="Solicitante")
    is_traveler = models.BooleanField(default=False, verbose_name="Viajante")
    is_secretary = models.BooleanField(default=False, verbose_name="Secretária")

    class Meta:
        verbose_name = 'VIP'
        verbose_name_plural = 'VIPs'
        ordering = ['company_contact__name']

    def __str__(self):
        return f'{self.company_contact.company} - Vip: {self.company_contact.name}'
