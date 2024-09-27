import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()
from payment import TransactionType, PayableType, MainTransactionStatus, PaymentMode, TransactionStatus, PaymentMethod
from payment.models import AgreementPayment, Payment, SubPayment, AgreementPaymentDue
from account.models import Company, Dealer
from retailer.models import AgreementDue
from django.db import transaction
from django.utils import timezone
from company import ProgressStatus

'''
Can you mark these agreements as paid in the system; or if I can do it from backend I will do it as well>

298484	TX1137-35826	5TBBT54188S458841 	 Jeremy	 West	Limited Warranties	Full	---	 11/11/2023	 02/11/2024	 207.93	
298408	TX1137-35812	5FNRL5H68BB051092 	 Yadira	 Hernandez	Limited Warranties	Full	---	 11/10/2023	 02/10/2024	 207.93	
297905	TX1137-35661	1FTEW1C55JKE49195 	 Abelardo	 Moreno Salais	Limited Warranties	Full	---	 11/08/2023	 02/08/2024	 207.93	
297811	TX1137-35595	3GCUKREC3HG209713 	 Dontrel	 Riggins	Limited Warranties	Full	---	 11/06/2023	 02/06/2024	 207.93	
297604	TX1137-35512	2GCEC19C671677679 	 Jaime	 Escalante Perales	Limited Warranties	Full	---	 11/03/2023	 02/03/2024	 207.93	
297598	TX1137-35506	4T1BF1FK3DU266676 	 Maleya	 Harris	Limited Warranties	Full	---	 11/03/2023	 02/03/2024	 207.93	
297577	TX1137-35485	3GCPCREH7EG440227 
'''

dealer_id = 137
agreement_numbers = ["TX1137-35826","TX1137-35812","TX1137-35661", "TX1137-35595", "TX1137-35512", "TX1137-35506","TX1137-35485"]
dealer_obj = Dealer.objects.get(id=dealer_id)
with transaction.atomic():
    company = Company.objects.get(id=1)
    payment = Payment(
        company=company,
        external_admin=dealer_obj.external_admin,
        transaction_type=TransactionType.CREDIT,
        payable_type=PayableType.DEALER,
        payable_id=dealer_id,
        transaction_status=MainTransactionStatus.FULLPAYMENT,
        payment_mode=PaymentMode.ADMIN_PAID,
        status=ProgressStatus.SUCCESS,
        date=timezone.now(),
    )
    payment.save()
    total_amount = 0.00

    for agreement_due in AgreementDue.objects.filter(agreement__agreement_number__in=agreement_numbers, agreement__dealer__id=dealer_id):
        amount = agreement_due.amount_due
        due_details = agreement_due.due_details
        agreement_due.amount_paid = agreement_due.amount_paid + amount
        agreement_due.amount_due = agreement_due.amount - agreement_due.amount_paid
        agreement_due.is_paid = True
        agreement_due.save()
        agreement_payment = AgreementPayment(
            payment=payment,
            payable_type=PayableType.DEALER,
            payable_id=dealer_id,
            agreement=agreement_due.agreement,
            date=timezone.now(),
            paid_amount=round(amount, 2),
        )
        agreement_payment.save()
        agreement_payment_due = AgreementPaymentDue(due=agreement_due, agreement_payment=agreement_payment, due_details=due_details)
        agreement_payment_due.save()
        total_amount += amount

    subpayment = SubPayment(
        amount=round(total_amount, 2),
        transaction_id="ChequePayment",
        transaction_status=TransactionStatus.PROCESSED,
        payment=payment,
        payment_method=PaymentMethod.CHEQUE,
    )
    payment.paid_amount = round(total_amount, 2)
    payment.save()
    subpayment.save()