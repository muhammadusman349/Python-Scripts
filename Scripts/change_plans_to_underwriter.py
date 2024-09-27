import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from retailer.models import Customer
from payment.models import AgreementPayment
from payment import PayableType
from payment.models import (
    AgreementPayment,
    CancellationPayment,
    ClaimPayment,
    AgreementMoneyMovementDue,
    CancellationMoneyMovementDue,
    ClaimMoneyMovementDue
    )
from payment.moneymovement.tasks import (
    create_underwriter_money_movement_dues,
    create_underwriter_cancellation_money_movement_dues,
    create_underwriter_claims_money_movement_dues
    )
""""
Here are the plans we need switched to Verisure Insurance Company:
2879,2878,2872,2871,2865,1178,1177,1168,1167,1158,1157,1087,1086

""""

plans_ids = 14
agreements = Customer.objects.filter(rate_card__subplan__plan__id=plans_ids)
for agreement in agreements:
    agreement_payments = AgreementPayment.objects.filter(agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER)
    if agreement_payments is None or agreement_payments.count() == 0:
        plan_underwriter = agreement.rate_card.subplan.plan.underwriter
        Customer.objects.filter(id=agreement.id).update(underwriter=plan_underwriter)

        # delete all underwriter unpaid moneymovement dues because clip type is changed
        AgreementMoneyMovementDue.objects.filter(agreement_payment__agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER, paid=False).delete()
        CancellationMoneyMovementDue.objects.filter(cancellation_payment__agreement_cancellation__agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER, paid=False).delete()
        ClaimMoneyMovementDue.objects.filter(claim_payment__agreement_claim__agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER, paid=False).delete()

        # Generate money movement dues for past agreements, claims, and cancellations
        agreement_payments = AgreementPayment.objects.filter(agreement=agreement, payable_type=PayableType.DEALER)
        for agreement_payment in agreement_payments:
            create_underwriter_money_movement_dues(agreement_payment, True)

        cancellation_payments = CancellationPayment.objects.filter(agreement_cancellation__agreement=agreement, payable_type=PayableType.DEALER)
        for cancellation_payment in cancellation_payments:
            create_underwriter_cancellation_money_movement_dues(cancellation_payment, True)

        claim_payments = ClaimPayment.objects.filter(agreement_claim__agreement=agreement, payable_type=PayableType.DEALER)
        for claim_payment in claim_payments:
            create_underwriter_claims_money_movement_dues(claim_payment, True)