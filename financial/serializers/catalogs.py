from rest_framework import serializers
from financial.catalogs import (
    Product,
    BillingCycle,
    BillingCalendar,
    PaymentMethod,
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class BillingCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingCycle
        fields = "__all__"


class BillingCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingCalendar
        fields = "__all__"


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"
