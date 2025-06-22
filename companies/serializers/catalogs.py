from rest_framework import serializers
from companies.catalogs import PointOfSale


class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = ["id", "name", "slug"]
        read_only_fields = ["slug"]
