from rest_framework import serializers
from companies.models import Company, CompanyContact, FeeDispatchContact
from financial.models import (
    ContractData,
    BillingPolicy,
    InvoiceConfig,
    FeeBilling,
    FeeDetails,
)


class ContractDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractData
        fields = "__all__"


class BillingPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingPolicy
        fields = "__all__"


class InvoiceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceConfig
        fields = "__all__"


class FinancialContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContact
        fields = "__all__"


class FeeBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeBilling
        fields = "__all__"


class FeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeDetails
        fields = "__all__"


class FeeDispatchContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeDispatchContact
        fields = "__all__"
