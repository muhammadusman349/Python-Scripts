# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
# import django
# django.setup()
# from company.models import Plan, Terms
# from payment.models import AgreementPayment, AgreementPaymentDue
# from payment import PayableType
# from retailer.models import Customer, AgreementDue
# from django.db import transaction
# from api.remittance import CLIP_TO_UNDERWRITER, RESERVE_TO_UNDERWRITER, ALL_AMOUNT_TO_UNDERWRITER

# t_ids = []
# term_ids=[43]
# terms = Terms.objects.filter(id__in=term_ids)
# terms = Terms.objects.all()
# with transaction.atomic():
#     for term in terms:
        # obligor_fee = term.obligor_fee
        # disabled = term.disabled
        # if disabled is False and obligor_fee > 0 :
        #     total_cost = term.admin_fee + term.agent_commission + term.misc_over_funds + term.over_funds + term.reserve + term.clip_fee + term.premium_tax + term.roadside + obligor_fee
        #     print("total_sum",total_cost)
        #     cost = total_cost - obligor_fee
        #     print("minus sum",cost)
        #     if term.cost == cost:
        #         print("done") 
        #         term_ids.append(term.id)
        #         Terms.objects.filter(id=term.id).update(cost=total_cost)
                
                # agreements = Customer.objects.filter(rate_card__id=term.id)
                # for agreement in agreements:
                #     print("agreeemenene",agreement.agreement_number)
                #     agreement_payment = AgreementPayment.objects.filter(agreement__id=agreement.id)
                #     if agreement_payment.count() != 0:
                #         # print('---dealer paid ---- ')
                #         dealer_paid = agreement_payment.filter(payable_type=PayableType.DEALER)
                #         moneymovements = agreement_payment.filter(payable_type=PayableType.UNDERWRITER).order_by('payment__id')
                #         for dealer in dealer_paid:
                #             print("dealerpayable",dealer.id)
                #         if dealer_paid.count() > 0 and moneymovements.count() == 0:        
                #             dues = agreement.agreementdue_set.all()
                #             for due in dues:
                #                 due_details = due.due_details
                            #     due_details['obligor_fee'] = agreement.get_data_field('obligor_fee')
                            #     print("duesss", due_details['obligor_fee'])
                            #     # Assuming 'amount_paid' is the key you want to update in the JSON field
                            #     amount = due.amount + agreement.get_data_field('obligor_fee')
                            #     amount_paid = due.amount_paid + agreement.get_data_field('obligor_fee')
                            #     AgreementDue.objects.filter(id=due.id).update(due_details=due_details, amount=amount, amount_paid=amount_paid)
                            #     print("Updated amount and amount_paid for AgreementDue id", due.id)

                        
                            # update agreement payment dues
                            # agreement_payment_dues = due.agreementpaymentdue_set.filter(agreement_payment__payable_type=PayableType.DEALER)
                            # for agreement_payment_due in agreement_payment_dues:
                            #     pay_due_details = agreement_payment_due.due_details
                            #     pay_due_details['obligor_fee'] = agreement.get_data_field('obligor_fee')
                            #     paid_amount = agreement_payment_due.agreement_payment.paid_amount + agreement.get_data_field('obligor_fee')
                            #     AgreementPaymentDue.objects.filter(id=agreement_payment_due.id).update(due_details=pay_due_details)
                            #     AgreementPayment.objects.filter(id=agreement_payment_due.agreement_payment.id).update(paid_amount=paid_amount)
                                            
                #          # update data if moneymovements is done
                #         elif dealer_paid.count() > 0 and moneymovements.count() > 0:
                #             # print('------ underwriter paid -----')
                #             # update agreement data
                #             data = agreement.data
                #             term = agreement.rate_card
                #             plan_cost = agreement.plan_cost + term.obligor_fee
                #             data['term']['cost'] = plan_cost
                #             Customer.objects.filter(id=agreement.id).update(data=data, plan_cost=plan_cost)

                #             # update dues
                #             dues = agreement.agreementdue_set.all()
                #             for due in dues:
                #                 due_details = due.due_details
                #                 due_details['obligor_fee'] = agreement.get_data_field('obligor_fee')
                #                 AgreementDue.objects.filter(id=due.id).update(due_details=due_details)

                #                 # update agreement payment dues
                #                 agreement_payment_dues = due.agreementpaymentdue_set.filter(agreement_payment__payable_type=PayableType.UNDERWRITER)
                #                 for agreement_payment_due in agreement_payment_dues:
                #                     pay_due_details = agreement_payment_due.due_details
                #                     pay_due_details['obligor_fee'] = agreement.get_data_field('obligor_fee')
                #                     AgreementPaymentDue.objects.filter(id=agreement_payment_due.id).update(due_details=pay_due_details)
                #             for moneymovement in moneymovements:
                #                 # to get old amount we use reference id
                #                 reference_payment = AgreementPayment.objects.get(id=moneymovement.reference_id)
                #                 dealer_detail_receipt = reference_payment.detail_receipt()["receipt"]

                #                 paid_amount = 0
                #                 if moneymovement.agreement.clip_type in ALL_AMOUNT_TO_UNDERWRITER:
                #                     paid_amount += dealer_detail_receipt['obligor_fee']  + dealer_detail_receipt["total_surcharge"]
                #                 if moneymovement.agreement.clip_type in RESERVE_TO_UNDERWRITER:
                #                     paid_amount += dealer_detail_receipt["reserve"]+ dealer_detail_receipt["premium_tax"]+ dealer_detail_receipt["total_surcharge"]

                #                 if moneymovement.agreement.clip_type in CLIP_TO_UNDERWRITER:
                #                     paid_amount += dealer_detail_receipt["clip_fee"]
                                                                                  
                #                 moneymovement.paid_amount = paid_amount
                #                 moneymovement.save()

                    # else:
                    #     # update agreement data
                    #     # print('---- unpaid ---- ')
                    #     data = agreement.data
                    #     term = agreement.rate_card
                    #     plan_cost = agreement.plan_cost + term.obligor_fee
                    #     data['term']['cost'] = plan_cost
                    #     Customer.objects.filter(id=agreement.id).update(data=data, plan_cost=plan_cost)
                    

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django

django.setup()
from company.models import Terms
from payment.models import Payment, SubPayment, AgreementPayment, AgreementPaymentDue
from payment import PayableType
from retailer.models import Customer, AgreementDue
from django.db import transaction

term_ids = [52]
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
        print("total_cost",total_cost)
        cost = total_cost - obligor_fee
        print("cost_diff",cost)
        if term.cost == cost and total_cost != term.cost:
            print("Term Cost This condition True")
            Terms.objects.filter(id=term.id).update(cost=total_cost)
            print("Term cost updated")
            agreements = Customer.objects.filter(rate_card__id=term.id)
            for agreement in agreements:
                data = agreement.data
                agreement_plan_cost = agreement.plan_cost
                print("agre_plan_cost",agreement_plan_cost)
                total_plan_cost = (
                                   data['term']['reserve'] 
                                   + data['term']['clip_fee'] 
                                   + data['term']['premium_tax'] 
                                   + data['term']['over_funds'] 
                                   + data['term']['agent_commission']  
                                   + data['term']['admin_fee'] 
                                   + data['term']['roadside'] 
                                   + data['term']['obligor_fee']
                                   + data['term']['misc_over_funds']
                                   + agreement.total_surcharge
                                )
                print("total_plan_cost",total_plan_cost)
                agreement_cost = total_plan_cost - data['term']['obligor_fee'] - agreement.total_surcharge
                print("diff_agre",agreement_cost)
                if agreement_plan_cost == agreement_cost and total_plan_cost != agreement_plan_cost:
                    print("Agreement_Plan_Cost This condition True")
                    data['term']['cost'] = total_plan_cost
                    Customer.objects.filter(id=agreement.id).update(data=data, plan_cost=total_plan_cost)
                    print("Agreement plan cost updated")

                agreement_payments = AgreementPayment.objects.filter(agreement__id=agreement.id)
                if agreement_payments.exists():
                    dealer_paid = agreement_payments.filter(payable_type=PayableType.DEALER)
                    if dealer_paid.exists():
                        dues = agreement.agreementdue_set.all()
                        for due in dues:
                            amount = total_plan_cost #due.amount + obligor_fee
                            amount_paid = total_plan_cost #due.amount_paid + obligor_fee
                            print("amount_paid",amount_paid)
                            AgreementDue.objects.filter(id=due.id).update(amount=amount, amount_paid=amount_paid)
                            print("AgreementDue amount and amount_paid updated")

                            agreement_payment_dues = due.agreementpaymentdue_set.filter(agreement_payment__payable_type=PayableType.DEALER)
                            for agreement_payment_due in agreement_payment_dues:
                                paid_amount = total_plan_cost #agreement_payment_due.agreement_payment.paid_amount + obligor_fee
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