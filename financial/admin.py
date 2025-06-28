from django.contrib import admin
from .models import (
    ContractData,
    BillingPolicy,
    InvoiceConfig,
    FeeBilling,
    FeeDetails,
)
from .catalogs import (
    Product,
    BillingCycle,
    BillingCalendar,
    PaymentMethod,
)


class CompanyRelatedAdmin(admin.ModelAdmin):
    list_filter = ("company",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)


@admin.register(ContractData)
class ContractDataAdmin(CompanyRelatedAdmin):
    list_display = ("company", "signature_date", "expiration_date", "alert_contract")
    search_fields = ("company__name",)
    readonly_fields = ("status", "alert_contract")


@admin.register(BillingPolicy)
class BillingPolicyAdmin(CompanyRelatedAdmin):
    list_display = ("company", "get_products", "cycle", "term_days", "calendar")
    filter_horizontal = ("products_to_bill",)

    def get_products(self, obj):
        return ", ".join(p.product_type for p in obj.products_to_bill.all())
    get_products.short_description = "Produtos a Faturar"


@admin.register(InvoiceConfig)
class InvoiceConfigAdmin(CompanyRelatedAdmin):
    list_display = ("company", "creation_type", "has_cutoff")
    filter_horizontal = ("payment_methods",)


@admin.register(FeeBilling)
class FeeBillingAdmin(CompanyRelatedAdmin):
    list_display = ("company", "charge_type")
    filter_horizontal = ("products_to_charge",)


@admin.register(FeeDetails)
class FeeDetailsAdmin(CompanyRelatedAdmin):
    list_display = ("company", "fee_closing_date", "cycle", "payment_date", "send_report")
    search_fields = ("validation",)


# Models as Catalogs
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_type",)
    readonly_fields = ("slug",)


@admin.register(BillingCycle)
class BillingCycleAdmin(admin.ModelAdmin):
    list_display = ("days",)


@admin.register(BillingCalendar)
class BillingCalendarAdmin(admin.ModelAdmin):
    list_display = ("cycle_date",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("payment_type",)
    readonly_fields = ("slug",)
