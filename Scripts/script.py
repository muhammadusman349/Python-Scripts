import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from retailer.models import Customer, ReinsuranceDistributionAgreement
from company.models import Dealer
from payment import PayableType
from payment.models import Payment
from payment.moneymovement.tasks import generate_money_movement_due
from django.db import transaction

'''some agreements dealermart failure to perfom doesnt have resinusrance 
in distribution we need a script to check which agreements doesnt have distribution created 
and create distribution and then generate money movement dues for past agreements and claims and cancelations'''

dealer_id = 2
agreements = Customer.objects.filter(dealer__id=dealer_id)

agreements_without_distribution = []
created_agreement_reinsurance_distribution = []

with transaction.atomic():
    for agreement in agreements:
        if not ReinsuranceDistributionAgreement.objects.filter(agreement=agreement).exists():
            # If distribution doesn't exist for this agreement, create one
            reinsurance_dist_data = {
                "agreement": agreement,
                "plan": agreement.PlanObj,
                "reinsurance": agreement.reinsurance,
                "percentage": 100
            }
            reinsurance_distribution_agreement = ReinsuranceDistributionAgreement.objects.create(**reinsurance_dist_data)
            created_agreement_reinsurance_distribution.append(reinsurance_distribution_agreement.id)
        else:
            # If distribution exists, add the agreement to the list
            agreements_without_distribution.append(agreement)

        # Generate money movement dues for past payments associated with the agreement
        payments = Payment.objects.filter(payable_type=PayableType.DEALER, agreement=agreement)
        for p in payments:
            generate_money_movement_due(payment_id=p.id)

print("Agreements without distribution:", agreements_without_distribution)
print("Created agreement reinsurance distributions:", created_agreement_reinsurance_distribution)

