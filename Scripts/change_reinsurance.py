import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from retailer.models import Customer, ReinsuranceDistributionAgreement
from company.models import ReInsurance
from payment import PayableType
from payment.models import AgreementPayment
from api.remittance import ClipType


dealer_id = 3
old_reinsurance_id = 2

correct_reinsurance_id = 1
correct_reinsurance = ReInsurance.objects.get(id=correct_reinsurance_id)

agreements = Customer.objects.filter(dealer__id=dealer_id) 

for agreement in agreements:
    agreement_payments = AgreementPayment.objects.filter(agreement__id=agreement.id)
    if not agreement_payments.filter(payable_type=PayableType.REINSURANCE).exists():
        Customer.objects.filter(id=agreement.id).update(reinsurance=correct_reinsurance)
        if agreement.enable_money_movement is True and agreement.clip_type in (ClipType.FAILURE_TO_PERFORM, ClipType.DEALER_OBLIGOR, ClipType.DOWC, ClipType.LW_DEALEROBLIGOR):
            reinsurance_dist_agr = ReinsuranceDistributionAgreement.objects.filter(agreement__id=agreement.id, reinsurance__id=old_reinsurance_id).update(reinsurance=correct_reinsurance)

