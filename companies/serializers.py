from rest_framework import serializers
from companies.models import CompanyGroup, Company, Vip, CompanyContact, FeeDispatchContact


class GroupSerializer(serializers.ModelSerializer):
    main_company_name = serializers.CharField(
        source="main_company.name", read_only=True
    )

    class Meta:
        model = CompanyGroup
        fields = ["id", "name", "slug", "main_company", "main_company_name"]


class CompanySerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyGroup.objects.all(), write_only=True, source="group"
    )
    travel_managers = serializers.SerializerMethodField()
    account_executives = serializers.SerializerMethodField()
    billing_contacts = serializers.SerializerMethodField()
    fee_dispatch_contacts = serializers.SerializerMethodField()
    vip = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def get_travel_managers(self, obj):
        contacts = obj.companycontact.filter(is_travel_manager=True)
        return CompanyContactSerializer(contacts, many=True).data

    def get_account_executives(self, obj):
        contacts = obj.companycontact.filter(is_account_executive=True)
        return CompanyContactSerializer(contacts, many=True).data

    def get_billing_contacts(self, obj):
        contacts = obj.companycontact.filter(is_billing_contact=True)
        return CompanyContactSerializer(contacts, many=True).data

    def get_fee_dispatch_contacts(self, obj):
        contacts = FeeDispatchContact.objects.filter(company=obj)
        return FeeDispatchContactSerializer(contacts, many=True).data

    def get_vip(self, obj):
        vips = Vip.objects.filter(company_contact__company=obj)
        return VipSerializer(vips, many=True).data


class VipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vip
        fields = "__all__"


class CompanyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContact
        fields = "__all__"

    def validate_phone(self, value):
        return self._clean_phone_field(value, 10, "Telefone fixo")

    def validate_mobile(self, value):
        return self._clean_phone_field(value, 11, "Celular")

    def validate_whatsapp(self, value):
        return self._clean_phone_field(value, 11, "WhatsApp")

    def _clean_phone_field(self, value, expected_length, label):
        if not value:
            return value
        numeric = value.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        if len(numeric) != expected_length or not numeric.isdigit():
            raise serializers.ValidationError(
                f"{label} precisa conter {expected_length} dígitos: DDD e número"
            )
        return numeric


class FeeDispatchContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeDispatchContact
        fields = "__all__"

    def validate_invoice_to(self, value):
        if not value.is_billing_contact:
            raise serializers.ValidationError(
                "O contato selecionado não está marcado como 'Contato para Cobrança'."
            )
        return value
