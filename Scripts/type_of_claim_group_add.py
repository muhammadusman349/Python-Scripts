import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()
from company.models import SubPlan, TypeOfClaimGroup, VehicleType

# plan_ids = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
# subplans = SubPlan.objects.filter(plan__id__in=plan_ids)

# for subplan in subplans:
#     if subplan.type_of_claim_group:
#         if subplan.plan.vehicle_type == VehicleType.AUTO:
#             subplan.type_of_claim_group.vehicle_type = VehicleType.AUTO
#         elif subplan.plan.vehicle_type == VehicleType.RV:
#             subplan.type_of_claim_group.vehicle_type = VehicleType.RV
#         elif subplan.plan.vehicle_type == VehicleType.GOLFCART:
#             subplan.type_of_claim_group.vehicle_type = VehicleType.GOLFCART
#         elif subplan.plan.vehicle_type == VehicleType.MARINE:
#             subplan.type_of_claim_group.vehicle_type = VehicleType.MARINE
#         elif subplan.plan.vehicle_type == VehicleType.MOWER:
#             subplan.type_of_claim_group.vehicle_type = VehicleType.MOWER
#         elif subplan.plan.vehicle_type == VehicleType.POWERSPORTS:
#             subplan.type_of_claim_group.vehicle_type = VehicleType.POWERSPORTS
#         subplan.type_of_claim_group.save()

plan_vehicle_type_mapping = {
    10: VehicleType.AUTO,
    11: VehicleType.RV,
    12: VehicleType.GOLFCART,
    13: VehicleType.MARINE,
    14: VehicleType.MOWER,
    15: VehicleType.POWERSPORTS,
    # Add more mappings as needed
}

plan_ids = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
subplans = SubPlan.objects.filter(plan__id__in=plan_ids)

for subplan in subplans:
    if subplan.type_of_claim_group:
        plan_id = subplan.plan.id
        if plan_id in plan_vehicle_type_mapping:
            subplan.type_of_claim_group.vehicle_type = plan_vehicle_type_mapping[plan_id]
            subplan.type_of_claim_group.save()

        print("DOne........!",subplan.type_of_claim_group)
  