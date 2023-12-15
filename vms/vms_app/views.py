from .models import (Vendor, PurchaseOrder, HistoricalPerformance)
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import vender_serializer
from rest_framework.permissions import IsAuthenticated
from vms_app.utils import *
from django.utils import timezone
import logging

_logger = logging.getLogger(__name__)

class VendorsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            qs = Vendor.objects.filter(id=id)
        else:
            qs = Vendor.objects.all()
        serializer = vender_serializer.VendorSerializer(qs, many=True)        
        resp = parse_response(serializer.data, status=status.HTTP_200_OK)
        return Response(resp)
    
    def post(self, request):
        user = request.user
        request.data.update({'user':user.id})
        serializer = vender_serializer.VendorSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            resp = parse_response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(resp)
        return Response(parse_error(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
        
    def put(self, request, id):
        vendor = get_instance(Vendor, id)
        if vendor:
            serializer = vender_serializer.VendorSerializer(vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                resp = parse_response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(resp)
            return Response(parse_error(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
        return Response(parse_response(status=status.HTTP_404_NOT_FOUND))
    
    def delete(self, request, id):
        vendor = get_instance(Vendor, id)
        if vendor:
            vendor.delete()
            return Response(parse_response(status=status.HTTP_200_OK))
        return Response(parse_response(status=status.HTTP_404_NOT_FOUND))


# purchase order view
class PurchaseOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        data = self.add_params(data)
        data.update({'user':request.user.id})
        serializer = vender_serializer.PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp = parse_response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(resp)
        return Response(parse_error(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
    
    def get(self, request, po_id=None):
        
        try:
            params = request.GET.copy()
            if po_id:
                pos = PurchaseOrder.objects.filter(id=po_id)
            else:
                if params.get('status'):
                    pos = PurchaseOrder.objects.filter(status=status)
                else:
                    pos = PurchaseOrder.objects.all()
            
            # filter by vendor
            if params.get('vender','').strip():
                vendor_id = params.get('vender','').strip()
                vendor = get_instance(Vendor, vendor_id)
                pos = pos.filter(vendor_id=vendor)
            
            serializer = vender_serializer.PurchaseOrderSerializer(pos, many=True)
            resp = parse_response(serializer.data, status=status.HTTP_200_OK)
            return Response(resp)
        except Exception as exc:
            _logger.error(f"Error:{exc}")
            return Response(parse_error(status=status.HTTP_400_BAD_REQUEST))
        
    def put(self, request, po_id):
        try:
            data = request.data        
            # parse date
            if 'delivery_date' in data:
                data.update({'delivery_date':parse_date(data.get('delivery_date'))})
            
            user = request.user
            data.update({'user':user})
            po = get_instance(PurchaseOrder, po_id)
            if  po and po.acknowledgment_date and po.status=='pending':
                serializer = vender_serializer.PurchaseOrderSerializer(po, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    resp = parse_response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(resp)
                return Response(parse_error(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
            return Response(parse_response(status=status.HTTP_400_BAD_REQUEST))
        except Exception as exc:
            _logger.error(f"Unable to update order. Error: {exc}")
            return Response(parse_error(status="Something went wrong."))
    
    def delete(self, request, po_id):
        po = get_instance(PurchaseOrder, po_id)
        if po:
            po.delete()
            return Response(parse_response(status=status.HTTP_200_OK))
        return Response(parse_response(status=status.HTTP_404_NOT_FOUND))
    
    def add_params(self, data):
        po_number = get_po_number()
        delivery_date = parse_date(data.get('delivery_date'))
        quantity = total_quantity(data.get('items'))
        data.update({
            'po_number':po_number,
            'delivery_date':delivery_date,
            'quantity': quantity,
            'issue_date': timezone.now() 
            })
        return data


class AcknowledgePOAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, po_id):        
        po = get_instance(PurchaseOrder, po_id)
        if po and po.status == 'pending':
            data = {'acknowledgment_date': timezone.now()}
            serializer = vender_serializer.PurchaseOrderSerializer(
                po, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                resp = parse_response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(resp)
            return Response(parse_error(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
        return Response(parse_response(status=status.HTTP_400_BAD_REQUEST))


class VendorsPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        vendor = Vendor.objects.get(id=id)
        if vendor:
            serializer = vender_serializer.VendorPerformanceSerializer(vendor)
            resp = parse_response(serializer.data, status=status.HTTP_200_OK)
            return Response(resp)
        return Response(parse_response(status=status.HTTP_404_NOT_FOUND))


class VendorsPerformanceHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            id=int(id)
            vendor = get_instance(Vendor, id)
            if vendor:                
                ven_his = HistoricalPerformance.objects.filter(vendor=vendor).order_by('-date')
                if ven_his:
                    data = vender_serializer.VendorHistoricalPerformanceSerializer(ven_his, many=True).data
                    resp = parse_response(data, status=status.HTTP_200_OK)
                    return Response(resp)
            return Response(parse_response(status=status.HTTP_404_NOT_FOUND))
        except Exception as exc:
            _logger.error(f"Con't get Vendor {id} performnce history. Error :{exc}")
            return Response(parse_response(status=status.HTTP_404_NOT_FOUND))
            
