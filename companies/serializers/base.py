from rest_framework import serializers
from companies.catalogs import PointOfSale
from companies.models import CompanyGroup, Company, Vip
from companies.serializers.catalogs import PointOfSaleSerializer
from companies.serializers.contact import VipSerializer, CompanyContactSerializer, FeeDispatchContactSerializer
from financial.serializers.base import (
    ContractDataSerializer, BillingPolicySerializer, InvoiceConfigSerializer,
    FeeBillingSerializer, FeeDetailsSerializer
)


class CompanySerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=CompanyGroup.objects.all(), write_only=True
    )
    group_name = serializers.CharField(source="group.name", read_only=True)
    point_of_sale = PointOfSaleSerializer(read_only=True)
    point_of_sale_id = serializers.PrimaryKeyRelatedField(
        queryset=PointOfSale.objects.all(), write_only=True, source="point_of_sale"
    )

    travel_managers = serializers.SerializerMethodField()
    account_executives = serializers.SerializerMethodField()
    billing_contacts = serializers.SerializerMethodField()
    fee_dispatch_contacts = serializers.SerializerMethodField()
    vip = serializers.SerializerMethodField()

    contract_data = serializers.SerializerMethodField()
    billing_policy = serializers.SerializerMethodField()
    invoice_config = serializers.SerializerMethodField()
    fee_billing = serializers.SerializerMethodField()
    fee_details = serializers.SerializerMethodField()

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
        return FeeDispatchContactSerializer(obj.feedispatchcontact.all(), many=True).data

    def get_vip(self, obj):
        vips = Vip.objects.filter(company_contact__company=obj)
        return VipSerializer(vips, many=True).data

    def get_contract_data(self, obj):
        return ContractDataSerializer(obj.contractdata.all(), many=True).data

    def get_billing_policy(self, obj):
        return BillingPolicySerializer(obj.billingpolicy.all(), many=True).data

    def get_invoice_config(self, obj):
        return InvoiceConfigSerializer(obj.invoiceconfig.all(), many=True).data

    def get_fee_billing(self, obj):
        return FeeBillingSerializer(obj.feebilling.all(), many=True).data

    def get_fee_details(self, obj):
        return FeeDetailsSerializer(obj.feedetails.all(), many=True).data


class GroupSerializer(serializers.ModelSerializer):
    main_company_name = serializers.CharField(
        source="main_company.name", read_only=True
    )

    def get_companies(self, obj):
        return CompanySerializer(obj.companies.all(), many=True).data

    companies = serializers.SerializerMethodField()

    class Meta:
        model = CompanyGroup
        fields = ["id", "name", "main_company", "main_company_name", "companies"]

