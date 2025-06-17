from django.core.exceptions import ValidationError
from django.db import models
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


class Company(models.Model):
    name = models.CharField('Razão Social', max_length=255, help_text='Nome jurídico oficial')
    fantasy_name = models.CharField('Nome Fantasia', max_length=255, help_text='Nome utilizado comercialmente')
    cnpj = models.CharField('CNPJ', max_length=14, help_text='Validação obrigatória')
    full_address = models.TextField(
        'Endereço Completo', blank=True, null=True, help_text='Utilizado para referência e notas fiscais'
    )
    segment = models.CharField('Segmento', max_length=255, help_text='Ex: Saúde, Educação, Indústria')
    benner_code = models.CharField(
        'Código Interno (Benner)', max_length=255, help_text='Código cadastrado no sistema Benner'
    )
    obt_link = models.CharField('Link do OBT', max_length=255, help_text='Endereço da Argo ou outro OBT')
    website = models.CharField('Site', max_length=255, blank=True, null=True, help_text='Página institucional')
    travel_manager_name = models.CharField(
        'Nome do Gestor de Viagem', max_length=255, help_text='Contato principal e backups'
    )
    travel_manager_email = models.EmailField(
        'Email do Gestor de Viagem', max_length=255, help_text='Contato principal e backups'
    )
    management_phone = models.CharField('Telefone Fixo da Gestão', max_length=255, help_text='Telefone fixo')
    management_mobile_phone = models.CharField('Telefone Móvel da Gestão', max_length=255, help_text='Telefone móvel')
    account_executive = models.CharField('Executivo de Contas', max_length=255, help_text='Representante da agência')
    observations = models.TextField(
        'Observações/Particularidades', blank=True, null=True, help_text='Regras específicas por cliente'
    )

    class Meta:
        verbose_name = 'Companhia'
        verbose_name_plural = 'Companhias'
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

    def save(self, *args, **kwargs):
        self.full_clean()  # Chama o clean acima, e os campos já serão formatados
        super().save(*args, **kwargs)


class VipSecretaries(CompanyRelatedModel):
    name = models.CharField('Nome', max_length=255)
    company_name = models.CharField('Empresa', max_length=255)
    secretary_allocation = models.CharField('Alocação Secretária', max_length=255)
    executives_served = models.CharField('Excutivos atendidos', max_length=255)
    public_tower = models.TextField('Torre / Público')
    email = models.EmailField('E-mail', max_length=255)

    class Meta:
        verbose_name = 'VIP Secretaria'
        verbose_name_plural = 'VIP Secretarias'
        ordering = ['name']

    def __str__(self):
        return self.name
