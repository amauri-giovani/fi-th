from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from companies.catalogs import PointOfSale
from companies.models import CompanyGroup, Company, CompanyContact, FeeDispatchContact, Vip
from companies.serializers.base import GroupSerializer, CompanySerializer
from companies.serializers.catalogs import PointOfSaleSerializer
from companies.serializers.contact import CompanyContactSerializer, FeeDispatchContactSerializer, VipSerializer


class GroupViewSet(ModelViewSet):
    queryset = CompanyGroup.objects.select_related("main_company").prefetch_related(
        Prefetch(
            "companies",
            queryset=Company.objects.select_related("point_of_sale").prefetch_related(
                "companycontact__vips",
                "feedispatchcontact",
                "contractdata",
                "billingpolicy",
                "invoiceconfig",
                "feebilling",
                "feedetails",
            )
        )
    )
    serializer_class = GroupSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get_queryset(self):
        queryset = Company.objects.all()
        group_id = self.request.query_params.get("group")
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                output_serializer = self.get_serializer(instance)
                return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"detail": "Erro ao salvar a empresa. Por favor, tente novamente ou contate o suporte."},
                status=status.HTTP_400_BAD_REQUEST
            )


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
