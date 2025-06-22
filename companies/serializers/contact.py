from rest_framework import serializers
from companies.models import Vip, CompanyContact, FeeDispatchContact


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
