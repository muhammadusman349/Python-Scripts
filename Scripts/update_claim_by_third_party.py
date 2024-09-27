import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from retailer.models import CustomerClaim 
from account.models import RepairFacility

"""
This claim was accidently paid to the dealership instead of the repair facility Nanos Auto.  
I had to manually void in CPx and then reissue the payment.  
Can you fix it so it shows NANOS was the company getting the payment?
TX1001-11662-C2471 

"""

claim_number = "DX1003-10093-C20"       # for test
repair_facility_number = "RF1001"       # for test

RF = RepairFacility.objects.get(repair_facility_number=repair_facility_number)
CustomerClaim.objects.filter(claim_number=claim_number).update(by_third_party=True, third_party=RF)
