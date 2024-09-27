import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from django.db import transaction
from retailer.models import Customer
from company.models import Plan, SubPlan, Terms

plans = Plan.objects.all()
with transaction.atomic():
    for plan in plans:
        if plan.disabled and not Customer.objects.filter(rate_card__subplan__plan=plan).exists():
            terms=  Terms.objects.filter(subplan__plan=plan)
            subplans =  SubPlan.objects.filter(plan=plan)
            for t in terms:
                print("t",t.name)
                t.delete()
            for s in subplans:
                print("s",s.name)
                s.delete()
            plan.delete()