from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.utils import timezone
import uuid

def parse_response(data={}, status=1):
    res = {
        'status': status,
        'message': 'ok',
        'data':data
    }
    return res

def parse_error(e, status=0):
    return  {
        'status': status,
        'message': e,
        'data':{}
    }

def get_instance(_Model, id):
    try:
        return _Model.objects.get(id=id)
    except _Model.DoesNotExist:
        return None

def vendor_auth_token(vendor_name):
    from .models import Vendor    
    vendor = Vendor.objects.get(username=vendor_name)
    token, created = Token.objects.get_or_create(user=vendor)
    return token.key

def get_po_number():
    from .models import PurchaseOrder
    order_id = str(uuid.uuid4().hex[:12]).upper()
    while PurchaseOrder.objects.filter(po_number=order_id).exists():
        order_id = str(uuid.uuid4().hex[:10]).upper()
    return order_id

def parse_date(date):
    date_format = '%Y-%m-%d'
    if not date:
        date = timezone.now() + timedelta(days=7)
        return date
    date = datetime.strptime(date, date_format)
    return date

def total_quantity(value):
    total=0
    for key, val in value.items():
            if not isinstance(val, (int, float)):
                raise ValidationError(F"Item '{key}' value must be in int or float.")    
            else:                
                total = total + val
    return total