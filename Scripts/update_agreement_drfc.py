import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from retailer.models import Customer

agreement_numbers = ["MD1105-32174", "MD1105-32173"]
drfc_values = [1239, 3900]

agreements = Customer.objects.filter(agreement_number__in=agreement_numbers)
for agreement, drfc in zip(agreements, drfc_values):
    Customer.objects.filter(id=agreement.id).update(DRFC=drfc)
