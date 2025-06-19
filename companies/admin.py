from django.contrib import admin
from .models import CompanyGroup, Company, CompanyContact, FeeDispatchContact, Vip


@admin.register(CompanyGroup)
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "main_company__name")
    search_fields = ("name", "slug", "main_company__name")
    ordering = ("name",)
    readonly_fields = ("slug",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "cnpj", "segment", "benner_code")
    search_fields = ("name", "cnpj", "fantasy_name")
    ordering = ("name",)


@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):
    list_display = (
        "company", "name", "role", "email",
        "is_travel_manager", "is_account_executive", "is_billing_contact"
    )
    list_filter = ("company", "is_travel_manager", "is_account_executive", "is_billing_contact")
    search_fields = ("name", "email", "role")


@admin.register(FeeDispatchContact)
class FeeDispatchContactAdmin(admin.ModelAdmin):
    list_display = ("company", "invoice_to")
    list_filter = ("company",)
    search_fields = ("invoice_to__name",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "invoice_to":
            kwargs["queryset"] = CompanyContact.objects.filter(is_billing_contact=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Vip)
class VipAdmin(admin.ModelAdmin):
    list_display = ("company_contact", "is_requester", "is_traveler", "is_secretary")
    list_filter = ("company_contact", "is_requester", "is_traveler", "is_secretary")
    search_fields = ("company_contact__name",)
