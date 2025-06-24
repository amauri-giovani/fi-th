from rest_framework import serializers
from companies.catalogs import PointOfSale
from companies.models import CompanyGroup, Company, Vip, CompanyContact
from companies.serializers.catalogs import PointOfSaleSerializer
from companies.serializers.contact import VipSerializer, CompanyContactSerializer, FeeDispatchContactSerializer
from financial.models import ContractData
from financial.serializers.base import (
    ContractDataSerializer, BillingPolicySerializer, InvoiceConfigSerializer,
    FeeBillingSerializer, FeeDetailsSerializer
)


class GroupNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyGroup
        fields = ["id", "name"]


class CompanySerializer(serializers.ModelSerializer):
    group = GroupNestedSerializer(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyGroup.objects.all(),
        write_only=True,
        source="group"
    )
    group_name = serializers.CharField(source="group.name", read_only=True)
    account_executive_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyContact.objects.all(),
        source="account_executive",
        write_only=True,
        required=False,
        allow_null=True
    )
    current_contract_id = serializers.PrimaryKeyRelatedField(
        queryset=ContractData.objects.all(),
        source="current_contract",
        write_only=True,
        required=False,
        allow_null=True
    )
    point_of_sale = PointOfSaleSerializer(read_only=True)
    point_of_sale_id = serializers.PrimaryKeyRelatedField(
        queryset=PointOfSale.objects.all(), write_only=True, source="point_of_sale"
    )

    travel_managers = serializers.SerializerMethodField()
    billing_contacts = serializers.SerializerMethodField()
    financial_contact = serializers.SerializerMethodField()
    commercial_contact = serializers.SerializerMethodField()
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

    def get_billing_contacts(self, obj):
        contacts = obj.companycontact.filter(is_billing_contact=True)
        return CompanyContactSerializer(contacts, many=True).data

    def get_financial_contact(self, obj):
        contacts = obj.companycontact.filter(is_financial_contact=True)
        return CompanyContactSerializer(contacts, many=True).data

    def get_commercial_contact(self, obj):
        contacts = obj.companycontact.filter(is_commercial_contact=True)
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

    def validate(self, attrs):
        company = self.instance or None  # None no create
        account_exec = attrs.get("account_executive")
        current_contract = attrs.get("current_contract")

        company_id = self.initial_data.get("id") or (company.id if company else None)

        if account_exec and account_exec.company_id != company_id:
            raise serializers.ValidationError({
                "account_executive_id": "O executivo deve pertencer à empresa."
            })

        if current_contract and current_contract.company_id != company_id:
            raise serializers.ValidationError({
                "current_contract_id": "O contrato deve pertencer à empresa."
            })
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    main_company_name = serializers.CharField(
        source="main_company.name", read_only=True
    )
    companies = serializers.SerializerMethodField()

    class Meta:
        model = CompanyGroup
        fields = ["id", "name", "main_company", "main_company_name", "companies"]

    def get_companies(self, obj):
        return CompanySerializer(obj.companies.all(), many=True).data

    def validate(self, data):
        main_company = data.get("main_company")
        group = self.instance

        if main_company and not main_company.group_id == group.id:
            raise serializers.ValidationError({
                "main_company": "A empresa principal deve pertencer a este grupo."
            })
        return data
