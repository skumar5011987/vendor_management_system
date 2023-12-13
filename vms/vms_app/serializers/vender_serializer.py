from rest_framework import serializers
from vms_app.models import (Vendor, PurchaseOrder, HistoricalPerformance)

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        # fields = '__all__'
        exclude = [
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate',
            'user'
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'name',
            'vendor_code',
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate'
            ]