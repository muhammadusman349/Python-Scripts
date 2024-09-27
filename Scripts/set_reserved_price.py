import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()
from retailer.models import Customer,AgreementDue

# Set dealer
agreement_numbers = ['MD1107-35360','MD1107-35306','MD1107-35289','MD1107-35170','MD1107-35098','MD1107-34307','MD1107-34235','MD1107-33997','MD1107-33908','MD1107-34008','MD1107-34197','MD1107-35285']
agreement_numbers = ['TX1001-10014'] 
agreement = Customer.objects.filter(agreement_number__in=agreement_numbers).update(dealer=108)

# Set Remit price

agreement_number= [('MD1105-32772',4165,5710),
                    'MD1105-32835','MD1105-32870','MD1105-32242','MD1105-32174','MD1105-32092','MD1105-32803','MD1105-32677','MD1105-32733','MD1105-32141','MD1105-32137','MD1105-32687','MD1105-31677']
remit_value = [4165,1230,1734,1734,1734,1734,1504,1504,1234,1234,1234,1099,1099]
ls_value = [5710,960,1504,1504,1504,1504,1234,1234,1099,1099,1099,960,960]

agreements = Customer.objects.filter(agreement_number__in=agreement_number)
for agreement in agreements:
    term = agreement.rate_card
    reserve = term.reserve
    plan_cost = agreement.plan_cost
    data = agreement.data
    remit = agreement.remit_value

    #difference
    difference = ls_value - remit_value
    new_reserve = difference + reserve

    data['term']['reserve'] = new_reserve
    plan_cost = data['term']['admin_fee'] + data['term']['agent_commission']+data['term']['misc_over_funds']+data['term']['over_funds']+data['term']['clip_fee']+data['term']['premium_tax']+data['term']['reserve']
    Customer.objects.filter(id=agreement.id).update(data=data,plan_cost=plan_cost)

    AgreementDue.objects.filter(agreement__id=agreement.id).delete()
    customer = Customer.objects.get(id=agreement.id)
    customer.save()