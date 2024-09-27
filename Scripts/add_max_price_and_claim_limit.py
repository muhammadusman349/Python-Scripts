import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()
from company.models import SubPlan, Terms
from company.utils import AGREEMENTSUBTYPECHOICES
from company.__init__ import VehicleType

'''
 I will give the plans/sub plans that should be $5000 for Claim Limit and $5000 total.  
 The Rest of the VSC contracts should be NADA.
 All Powersports VSC should be NADA Value.
 All RV should have the limits posted in the plans...if not we will correct manually.

'''

# For Plan Ids
plan_ids = [1,2,3]
subplans = SubPlan.objects.filter(plan__id__in=plan_ids).update(claim_limit_of_liability=5000)
term = Terms.objects.filter(subplan__plan__id__in=plan_ids).update(max_price=5000)

# The Rest of the VSC and All Powersports VSC contracts should be NADA
subplan = SubPlan.objects.filter(plan__vehicle_type=VehicleType.POWERSPORTS,plan_subtype=AGREEMENTSUBTYPECHOICES.VSC)
subplan.exclude(plan__id__in=plan_ids).update(is_nada_claim_limit_of_liability=True)


# For Subplan Ids
subplan_ids = [1,2,3]
subplans = SubPlan.objects.filter(id__in=subplan_ids).update(claim_limit_of_liability=5000)
term = Terms.objects.filter(subplan__id__in=subplan_ids).update(max_price=5000)

# The Rest of the VSC and All Powersports VSC contracts should be NADA
subplan = SubPlan.objects.filter(plan__vehicle_type=VehicleType.POWERSPORTS,plan_subtype=AGREEMENTSUBTYPECHOICES.VSC)
subplan.exclude(id__in=subplan_ids).update(is_nada_claim_limit_of_liability=True)



# plan_ids = [1,2,3]
# subplans = SubPlan.objects.filter(plan__id__in=plan_ids)
# for subplan in subplans:
#     if subplan.claim_limit_of_liability is None or subplan.claim_limit_of_liability < 5000:
#         subplan.claim_limit_of_liability == 5000
#         subplan.save()
#         term = Terms.objects.filter(subplan__plan__id__in=plan_ids).update(max_price=5000)



# subplan_ids = [1,2,3]
# subplans = SubPlan.objects.filter(id__in=subplan_ids)
# for subplan in subplans:
#     if subplan.claim_limit_of_liability is None or subplan.claim_limit_of_liability < 5000:
#         subplan.claim_limit_of_liability == 5000
#         subplan.save()
#         term = Terms.objects.filter(subplan__id__in=subplan_ids).update(max_price=5000)

# All Powersports VSC should be NADA Value
# vehicle_types = [VehicleType.POWERSPORTS, VehicleType.RV]
# plans = Plan.objects.filter(Q(vehicle_type__in=vehicle_types))
# SubPlan.objects.filter(plan__in=plans,plan_subtype=AGREEMENTSUBTYPECHOICES.VSC).update(is_nada_claim_limit_of_liability=True)