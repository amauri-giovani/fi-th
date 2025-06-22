from rest_framework import viewsets
from companies.catalogs import PointOfSale
from companies.models import CompanyGroup, Company, CompanyContact, FeeDispatchContact, Vip
from companies.serializers.base import GroupSerializer, CompanySerializer
from companies.serializers.catalogs import PointOfSaleSerializer
from companies.serializers.contact import CompanyContactSerializer, FeeDispatchContactSerializer, VipSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = CompanyGroup.objects.all()
    serializer_class = GroupSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyContactViewSet(viewsets.ModelViewSet):
    queryset = CompanyContact.objects.all()
    serializer_class = CompanyContactSerializer


class FeeDispatchContactViewSet(viewsets.ModelViewSet):
    queryset = FeeDispatchContact.objects.all()
    serializer_class = FeeDispatchContactSerializer


class VipViewSet(viewsets.ModelViewSet):
    queryset = Vip.objects.all()
    serializer_class = VipSerializer


class PointOfSaleViewSet(viewsets.ModelViewSet):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer
