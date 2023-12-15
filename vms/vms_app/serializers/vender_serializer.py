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
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['order_date'] =  instance.order_date.strftime('%d-%m-%Y')
        representation['delivery_date'] =  instance.delivery_date.strftime('%d-%m-%Y')
        representation['issue_date'] =  instance.issue_date.strftime('%d-%m-%Y') 
        representation['acknowledgment_date'] =  \
        instance.acknowledgment_date.strftime('%d-%m-%Y') if instance.acknowledgment_date else None
        
        
        return representation

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
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['on_time_delivery_rate'] = str(instance.on_time_delivery_rate) + ' %'
        representation['quality_rating_avg'] = str(instance.quality_rating_avg) + ' %'
        representation['average_response_time'] = str(instance.average_response_time) + ' hours'
        representation['fulfillment_rate'] = str(instance.fulfillment_rate) + ' %'
        
        return representation
    
class VendorHistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'