import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django

django.setup()
from company.models import Terms
from payment.models import Payment, SubPayment, AgreementPayment, AgreementPaymentDue
from payment import PayableType
from retailer.models import Customer, AgreementDue
from django.db import transaction

term_ids = [50]
terms = Terms.objects.filter(id__in=term_ids, disabled=False, obligor_fee__gt=0)
for term in terms:
    print(term.name)
with transaction.atomic():
    for term in terms:
        obligor_fee = term.obligor_fee
        total_cost = (
            term.admin_fee
            + term.agent_commission
            + term.misc_over_funds
            + term.over_funds
            + term.reserve
            + term.clip_fee
            + term.premium_tax
            + term.roadside
            + obligor_fee
        )
        cost = total_cost - obligor_fee
        if term.cost == cost and total_cost != term.cost:
            Terms.objects.filter(id=term.id).update(cost=total_cost)
            print("Term cost updated")
            agreements = Customer.objects.filter(rate_card__id=term.id)
            for agreement in agreements:
                data = agreement.data
                term = agreement.rate_card
                plan_cost = agreement.plan_cost + term.obligor_fee
                data['term']['cost'] = plan_cost
                Customer.objects.filter(id=agreement.id).update(data=data, plan_cost=plan_cost)
                print("Agreement plan cost updated")

                agreement_payments = AgreementPayment.objects.filter(agreement__id=agreement.id)
                if agreement_payments.exists():
                    dealer_paid = agreement_payments.filter(payable_type=PayableType.DEALER)
                    if dealer_paid.exists():
                        dues = agreement.agreementdue_set.all()
                        for due in dues:
                            amount = due.amount + obligor_fee
                            amount_paid = due.amount_paid + obligor_fee
                            AgreementDue.objects.filter(id=due.id).update(amount=amount, amount_paid=amount_paid)
                            print("AgreementDue amount and amount_paid updated")

                            agreement_payment_dues = due.agreementpaymentdue_set.filter(agreement_payment__payable_type=PayableType.DEALER)
                            for agreement_payment_due in agreement_payment_dues:
                                paid_amount = agreement_payment_due.agreement_payment.paid_amount + obligor_fee
                                AgreementPayment.objects.filter(id=agreement_payment_due.agreement_payment.id).update(paid_amount=paid_amount)
                                print("AgreementPayment paid_amount updated")
                                amount = paid_amount
                                print("SubPayment amount = paid_amount",amount)
                                SubPayment.objects.filter(payment__id=agreement_payment_due.agreement_payment.payment.id).update(amount=amount)
                                print("Subpayment updated")
                                paid_price = paid_amount
                                print("Payment paid_price = paid_amount",paid_price)
                                Payment.objects.filter(id=agreement_payment_due.agreement_payment.payment.id).update(paid_amount=paid_price)
                                print('Payment updated')
                    else:
                        print("No Dealer Payments found")
                        
                else:
                    print("No Agreement Payments found")