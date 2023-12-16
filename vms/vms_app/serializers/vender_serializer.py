from rest_framework import serializers
from django.core.validators import RegexValidator
from vms_app.models import (Vendor, PurchaseOrder, HistoricalPerformance)

class VendorSerializer(serializers.ModelSerializer):
    
    contact_details = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6789]\d{9}$',
                message='mobile numbers in India, which start with 6, 7, 8, or 9 and have 10 digits.'
            )
        ]
    )
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
    
    def validate(self, data):
        if data.get('issue_date') and data.get('delivery_date'):
            if data['delivery_date'] <= data['issue_date']:
                raise serializers.ValidationError("Delivery date must be greater than the issue date.")
            
        if data.get('quality_rating') is not None and 0 > data.get('quality_rating') > 100:
            raise serializers.ValidationError("Quality rating should be in between 1 to 100 or Null")
        return data
    
    def validate_items(self, value):
        for key, val in value.items():
            if not isinstance(val, (int, float)):
                raise serializers.ValidationError(f"The value Item '{key}' should be int or float.")
        return value
    
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