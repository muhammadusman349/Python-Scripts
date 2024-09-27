import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from payment.models import (
    AgreementPayment,
    CancellationPayment,
    ClaimPayment,
    AgreementMoneyMovementDue,
    CancellationMoneyMovementDue,
    ClaimMoneyMovementDue
)
from payment import PayableType

from retailer.models import (
    Customer,
    OverfundDistributionAgreement,
    MiscOverfundDistributionAgreement,
    AgentCommissionDistributionAgreement,
    AdminFeeDistributionAgreement,
    ReinsuranceDistributionAgreement,
    )
from payment.moneymovement.tasks import (
                    create_agreement_payment_money_movement_dues, 
                    create_cancellation_money_movement_dues, 
                    create_claim_money_movement_dues)
from api.remittance.__init__ import ClipType
from django.db import transaction


with transaction.atomic():
    # create distribution
    plan_id = 25
    agreements = Customer.objects.filter(rate_card__subplan__plan__id=plan_id, void=False)
    print('agreements.count  === ', agreements.count())
    agreement_enable_dist = []

    agent_dist = []
    overfund_dist = []
    misc_overfund_dist = []
    admin_fee_dist = []
    reinsurance_dist = []
    for agreement in agreements:
        agreement_payments = AgreementPayment.objects.filter(agreement__id=agreement.id)
        cancellation_payments = CancellationPayment.objects.filter(agreement_cancellation__agreement__id=agreement.id)
        claim_payments = ClaimPayment.objects.filter(agreement_claim__agreement__id=agreement.id)

        if agreement_payments.exclude(payable_type=PayableType.DEALER).exists() or cancellation_payments.exclude(payable_type=PayableType.DEALER).exists() or claim_payments.exclude(payable_type=PayableType.DEALER).exists():
            print('money movement is done -- ', agreement.id)
            continue

        plan = agreement.rate_card.subplan.plan
        if plan.enable_money_movement is True:
            Customer.objects.filter(id=agreement.id).update(clip_type=ClipType.DOLLAR_ONE)

            # create distribution
            dis_created = False
            agreement_agent_distribution = agreement.agent_commission_agreement.all()
            if agreement_agent_distribution.count() == 0:
                agent_distribution = plan.agent_commission_plan.all()
                for agent_dis_plan in agent_distribution:
                    agent_dis_ag = AgentCommissionDistributionAgreement()
                    agent_dis_ag.agreement = agreement
                    agent_dis_ag.plan = agent_dis_plan.plan
                    agent_dis_ag.agency = agent_dis_plan.agency
                    agent_dis_ag.member = agent_dis_plan.member
                    agent_dis_ag.percentage = agent_dis_plan.percentage
                    agent_dis_ag.save()
                    dis_created = True
                    agent_dist.append(agent_dis_ag.id)

            agreement_overfund_distribution = agreement.overfund_agreement.all()
            if agreement_overfund_distribution.count() == 0:
                overfund_distribution = plan.overfund_plan.all()
                for overfund_dis_plan in overfund_distribution:
                    overfund_dis_ag = OverfundDistributionAgreement()
                    overfund_dis_ag.agreement = agreement
                    overfund_dis_ag.plan = overfund_dis_plan.plan
                    overfund_dis_ag.member_of = overfund_dis_plan.member_of
                    overfund_dis_ag.member = overfund_dis_plan.member
                    overfund_dis_ag.percentage = overfund_dis_plan.percentage
                    overfund_dis_ag.save()
                    dis_created = True
                    overfund_dist.append(overfund_dis_ag.id)

            agreement_misc_overfund_distribution = agreement.misc_overfund_agreement.all()
            if agreement_misc_overfund_distribution.count() == 0:
                misc_overfund_distribution = plan.misc_overfund_plan.all()
                for misc_overfund_dis_plan in misc_overfund_distribution:
                    misc_overfund_dis_ag = MiscOverfundDistributionAgreement()
                    misc_overfund_dis_ag.agreement = agreement
                    misc_overfund_dis_ag.plan = misc_overfund_dis_plan.plan
                    misc_overfund_dis_ag.member_of = misc_overfund_dis_plan.member_of
                    misc_overfund_dis_ag.member = misc_overfund_dis_plan.member
                    misc_overfund_dis_ag.underwriter = misc_overfund_dis_plan.underwriter
                    misc_overfund_dis_ag.reinsurance = misc_overfund_dis_plan.reinsurance
                    misc_overfund_dis_ag.percentage = misc_overfund_dis_plan.percentage
                    misc_overfund_dis_ag.save()
                    dis_created = True
                    misc_overfund_dist.append(misc_overfund_dis_ag.id)

            agreement_reinsurance_distribution = agreement.reinsurancedistributionagreement_set.all()
            if agreement_reinsurance_distribution.count() == 0:
                reinsurance_distribution = plan.reinsurancedistribution_set.all()
                for reinsurance_dis_plan in reinsurance_distribution:
                    reinsurance_dis_ag = ReinsuranceDistributionAgreement()
                    reinsurance_dis_ag.agreement = agreement
                    reinsurance_dis_ag.plan = reinsurance_dis_plan.plan
                    reinsurance_dis_ag.reinsurance = reinsurance_dis_plan.reinsurance
                    reinsurance_dis_ag.percentage = reinsurance_dis_plan.percentage
                    reinsurance_dis_ag.save()
                    dis_created = True
                    reinsurance_dist.append(reinsurance_dis_ag.id)

            agreement_admin_fee_distribution = agreement.admin_fee_agreement.all()
            if agreement_admin_fee_distribution.count() == 0:
                admin_fee_distribution = plan.admin_fee_plan.all()
                for admin_fee_dis_plan in admin_fee_distribution:
                    admin_fee_dis_ag = AdminFeeDistributionAgreement()
                    admin_fee_dis_ag.agreement = agreement
                    admin_fee_dis_ag.plan = admin_fee_dis_plan.plan
                    admin_fee_dis_ag.member_of = admin_fee_dis_plan.member_of
                    admin_fee_dis_ag.member = admin_fee_dis_plan.member
                    admin_fee_dis_ag.percentage = admin_fee_dis_plan.percentage
                    admin_fee_dis_ag.save()
                    dis_created = True
                    admin_fee_dist.append(admin_fee_dis_ag.id)

            if dis_created == True:
                agreement_enable_dist.append(agreement.id)


         # delete all underwriter unpaid moneymovement dues because clip type is changed
        AgreementMoneyMovementDue.objects.filter(agreement_payment__agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER, paid=False).delete()
        CancellationMoneyMovementDue.objects.filter(cancellation_payment__agreement_cancellation__agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER, paid=False).delete()
        ClaimMoneyMovementDue.objects.filter(claim_payment__agreement_claim__agreement__id=agreement.id, payable_type=PayableType.UNDERWRITER, paid=False).delete()

        dealer_agreement_payments = agreement_payments.filter(payable_type=PayableType.DEALER)
        for agreement_payment in dealer_agreement_payments:
            agreement_moneymovement_dues = create_agreement_payment_money_movement_dues(agreement_payment, True)
            # print('agreement_moneymovement_dues = ', agreement_moneymovement_dues)

        dealer_cancellation_payment = cancellation_payments.filter(payable_type=PayableType.DEALER)
        for cancellation_payment in dealer_cancellation_payment:
            cancellation_moneymovement_dues = create_cancellation_money_movement_dues(cancellation_payment, True)
            # print('cancellation_moneymovement_dues = ', cancellation_moneymovement_dues)

        dealer_claim_payments = claim_payments.filter(payable_type=PayableType.DEALER)
        for claim_payment in dealer_claim_payments: 
            claim_moneymovement_dues = create_claim_money_movement_dues(claim_payment, True)
            # print('claim_moneymovement_dues = ', claim_moneymovement_dues)

print('agreement_enable_dist = ', agreement_enable_dist)
print('agreement_enable_dist len = ', len(agreement_enable_dist))
print('\n')
print('admin_fee_dist = ', admin_fee_dist)
print('admin_fee_dist len = ', len(admin_fee_dist))
print('\n')
print('reinsurance_dist = ', reinsurance_dist)
print('reinsurance_dist len= ', len(reinsurance_dist))
print('\n')
print('misc_overfund_dist = ', misc_overfund_dist)
print('misc_overfund_dist len= ', len(misc_overfund_dist))
print('\n')
print('overfund_dist = ', overfund_dist)
print('overfund_dist len= ', len(overfund_dist))
print('\n')
print('agent_dist = ', agent_dist)
print('agent_dist len= ', len(agent_dist))
