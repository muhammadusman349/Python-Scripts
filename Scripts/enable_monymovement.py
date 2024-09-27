import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()
from retailer.models import ( Customer,AdminFeeDistributionAgreement,
                             AgentCommissionDistributionAgreement,OverfundDistributionAgreement,
                             MiscOverfundDistributionAgreement,ReinsuranceDistributionAgreement)

'''
It's because the money movement was not done. 
Can you update this agreement and all past agreements  for plans 948, 949, 950, 951?

'''

plan_ids = [5]
agreement_enable_dist = []
agreements = Customer.objects.filter(rate_card__subplan__plan__id__in=plan_ids)
print('agreements count... ', agreements.count())
for agreement in agreements:
    if agreement.rate_card.subplan.plan.enable_money_movement:
        Customer.objects.filter(id=agreement.id).update(enable_money_movement=True)
    
        admin_fee_distribution = agreement.rate_card.subplan.plan.admin_fee_plan.all()
        for admin_distribution_plan in admin_fee_distribution:
            admin_fee_distribution_agreement = AdminFeeDistributionAgreement()
            admin_fee_distribution_agreement.agreement = agreement
            admin_fee_distribution_agreement.plan = admin_distribution_plan.plan
            admin_fee_distribution_agreement.member_of = admin_distribution_plan.member_of
            admin_fee_distribution_agreement.member = admin_distribution_plan.member
            admin_fee_distribution_agreement.percentage = admin_distribution_plan.percentage
            admin_fee_distribution_agreement.save()

        agent_distribution = agreement.rate_card.subplan.plan.agent_commission_plan.all()
        for agent_distribution_plan in agent_distribution:
            agent_distribution_agreement = AgentCommissionDistributionAgreement()
            agent_distribution_agreement.agreement = agreement
            agent_distribution_agreement.plan = agent_distribution_plan.plan
            agent_distribution_agreement.agency = agent_distribution_plan.agency
            agent_distribution_agreement.member = agent_distribution_plan.member
            agent_distribution_agreement.percentage = agent_distribution_plan.percentage
            agent_distribution_agreement.save()

        overfund_distribution = agreement.rate_card.subplan.plan.overfund_plan.all()
        for overfund_distribution_plan in overfund_distribution:
            overfund_distribution_agreement = OverfundDistributionAgreement()
            overfund_distribution_agreement.agreement = agreement
            overfund_distribution_agreement.plan = overfund_distribution_plan.plan
            overfund_distribution_agreement.member_of = overfund_distribution_plan.member_of
            overfund_distribution_agreement.member = overfund_distribution_plan.member
            overfund_distribution_agreement.percentage = overfund_distribution_plan.percentage
            overfund_distribution_agreement.save()

        misc_overfund_distribution = agreement.rate_card.subplan.plan.misc_overfund_plan.all()
        for misc_overfund_distribution_plan in misc_overfund_distribution:
            misc_overfund_distribution_agreement = MiscOverfundDistributionAgreement()
            misc_overfund_distribution_agreement.agreement = agreement
            misc_overfund_distribution_agreement.plan = misc_overfund_distribution_plan.plan
            misc_overfund_distribution_agreement.member_of = misc_overfund_distribution_plan.member_of
            misc_overfund_distribution_agreement.member = misc_overfund_distribution_plan.member
            misc_overfund_distribution_agreement.reinsurance = misc_overfund_distribution_plan.reinsurance
            misc_overfund_distribution_agreement.underwriter = misc_overfund_distribution_plan.underwriter
            misc_overfund_distribution_agreement.percentage = misc_overfund_distribution_plan.percentage
            misc_overfund_distribution_agreement.save()

        reinsurance_distribution = agreement.rate_card.subplan.plan.reinsurancedistribution_set.all()
        for reinsurance_distribution_plan in reinsurance_distribution:
            reinsurance_distribution_agreement = ReinsuranceDistributionAgreement()
            reinsurance_distribution_agreement.agreement = agreement
            reinsurance_distribution_agreement.plan = reinsurance_distribution_plan.plan
            reinsurance_distribution_agreement.reinsurance = reinsurance_distribution_plan.reinsurance
            reinsurance_distribution_agreement.percentage = reinsurance_distribution_plan.precentage
            reinsurance_distribution_agreement.save()

        agreement_enable_dist.append(agreement.id)