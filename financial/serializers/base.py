from rest_framework import serializers
from financial.models import ContractData, BillingPolicy, InvoiceConfig, FeeBilling, FeeDetails


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


class FeeBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeBilling
        fields = "__all__"


class FeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeDetails
        fields = "__all__"
