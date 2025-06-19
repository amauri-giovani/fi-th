from rest_framework import viewsets
from companies.serializers import CompanySerializer, VipSerializer
from companies.models import CompanyContact, FeeDispatchContact
from companies.serializers import Company, Vip, CompanyContactSerializer, FeeDispatchContactSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class VipViewSet(viewsets.ModelViewSet):
    queryset = Vip.objects.all()
    serializer_class = VipSerializer


class CompanyContactViewSet(viewsets.ModelViewSet):
    queryset = CompanyContact.objects.all()
    serializer_class = CompanyContactSerializer


class FeeDispatchContactViewSet(viewsets.ModelViewSet):
    queryset = FeeDispatchContact.objects.all()
    serializer_class = FeeDispatchContactSerializer
