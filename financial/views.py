from rest_framework import viewsets
from financial.models import (
    ContractData,
    BillingPolicy,
    InvoiceConfig,
    FeeBilling,
    FeeDetails,
)
from financial.serializers.base import (
    ContractDataSerializer,
    BillingPolicySerializer,
    InvoiceConfigSerializer,
    FeeBillingSerializer,
    FeeDetailsSerializer,
)


class ContractDataViewSet(viewsets.ModelViewSet):
    queryset = ContractData.objects.all()
    serializer_class = ContractDataSerializer


class BillingPolicyViewSet(viewsets.ModelViewSet):
    queryset = BillingPolicy.objects.all()
    serializer_class = BillingPolicySerializer


class InvoiceConfigViewSet(viewsets.ModelViewSet):
    queryset = InvoiceConfig.objects.all()
    serializer_class = InvoiceConfigSerializer


class FeeBillingViewSet(viewsets.ModelViewSet):
    queryset = FeeBilling.objects.all()
    serializer_class = FeeBillingSerializer


class FeeDetailsViewSet(viewsets.ModelViewSet):
    queryset = FeeDetails.objects.all()
    serializer_class = FeeDetailsSerializer
