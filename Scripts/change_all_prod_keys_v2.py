import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()
from account.models import Company, Dealer, ExternalAdministrator, Member, DwollaOtherAccount, LithicPayingClaimAccount, DwollaSenderSource
from company.models import ReInsurance, Underwriter
from company.utils import PAYMENTMETHODCHOICES
from dwolla.models import DwollaCustomer, DwollaFundingSourceV1
from dwolla import DwollaAccountType, DwollaCustomerOf

class ChangeProdData:
    def change_keys():
        DwollaSenderSource.objects.all().delete()
        company_obj = Company.objects.all()
        for com in company_obj:
            com.stripe_secret_key = 'sk_test_FicOoQJxyuoaCTIuEkAN7Bqm00BWSUEWVQ'
            com.stripe_public_key = 'pk_test_ceBrZ7GCSDhEJDNeXdXgx77n00ocK7lxed'

            com.dwolla_stagging = True
            com.dwolla_secret_key = 'jTIfrjN9qL4l2SEyFyoEkELeSqU6YYWAfCnKE4QRsEhlwJdqfB'
            com.dwolla_public_key = 'QZGOG8E42qRFCTgO3y7UPhnKhFFRgWKRvi7cCtwLxTtcSCCrWe'

            com.lithic_stagging = True
            com.lithic_api_key = '02a9ad5d-b4c3-413a-b667-c8313f8196f0'

            com.ck_stagging = True
            com.ck_username = 'DealAdminIO'
            com.ck_pass = 'qhg!@x7dai'
            com.ck_tpaCode = 'DAIO'

            com.motor_stagging = True
            com.motor_public_key = 'DaaSandbox'
            com.motor_private_key = '0wDK2hZHZ7NgdJTrb8xg1jPls'

            com.wis_inspection_stagging = True
            com.wis_username = 'DealAdminIO'
            com.wis_pass = 'qhg!@x7dai'
            com.save()
            print('company save')

    def delete_and_create_dummy_dwolla_accounts():
        company_obj = Company.objects.all()
        DwollaCustomer.objects.all().delete()
        DwollaFundingSourceV1.objects.all().delete()
        for com in company_obj:
            external_admin = ExternalAdministrator.objects.filter(company__id=com.id).first()

            # create dwolla main sending accounts
            main_dwolla_customer_data = {
                "company": com,
                "customer_type": DwollaAccountType.BUSINESS,
                "customer_id": "8a76c16d-6047-490c-b049-71c56de55079",
                "firstName": "{}-Superhero Savings Bank".format(com.name),
                "lastName": "sandbox",
                "email": "dealeradmin_buss@gmail.com",
                "businessName": "{}-Superhero Savings Bank".format(com.name),
                "status": "verified",
                "customer_of": DwollaCustomerOf.ADMIN,
                "address1": "bahria",
                "city": "isb",
                "state": "isb",
                "postalCode": "10001",
                "dateOfBirth": "1965-01-31",
                "social_security_number": "6789",
                "employer_identification_number": "00-0000000",
                }
            mian_dwolla_customer, created_main_cus = DwollaCustomer.objects.get_or_create(**main_dwolla_customer_data)

            main_dwolla_fs_data = {
                "nick_name": "{}-Superhero Savings Bank".format(com.name),
                "name": "{}-Superhero Savings Bank".format(com.name),
                "dwolla_customer": mian_dwolla_customer,
                "customer_fs_id": "8a76c16d-6047-490c-b049-71c56de55079",
                "routingNumber": "1111112121",
                "accountNumber": "121212121",
                "accountType": "Checking",
                "status": "verified",
                }
            mian_dwolla_fs, created_main_fs = DwollaFundingSourceV1.objects.get_or_create(**main_dwolla_fs_data)

            # set dwolla main account into external administrator sending and receiving source
            ExternalAdministrator.objects.filter(company__id=com.id).update(
                dwolla_sending_customer_account=mian_dwolla_customer,
                dwolla_sending_funding_source=mian_dwolla_fs,
                dwolla_receiving_account_type=DwollaAccountType.BUSINESS,
                dwolla_receiving_customer_account=mian_dwolla_customer,
                dwolla_receiving_funding_source=mian_dwolla_fs,
                )

            # create receive only customer and funding source
            receive_only_customer_data = {
                "company": com,
                "external_admin": external_admin,
                "customer_type": DwollaAccountType.RECEIVE_ONLY,
                "customer_id": "248242dd-6f90-4a2d-83ec-6123bccb0797",
                "firstName": "{}-RO".format(com.name),
                "lastName": "Sandbox",
                "email": "dealeradmin_ro@gmail.com",
                "businessName": "{}-RO".format(com.name),
                "status": "verified",
                }
            receive_only_customer, created = DwollaCustomer.objects.get_or_create(**receive_only_customer_data)

            receive_only_fs_data = {
                "nick_name": "{}-RO".format(com.name),
                "name": "{}-RO".format(com.name),
                'dwolla_customer': receive_only_customer,
                "customer_fs_id": "bbd5ebe5-3b49-4243-878e-ee9fdad75544",
                "routingNumber": "222222226",
                "accountNumber": "123456789",
                "accountType": "Checking",
                "status": "verified",
                }

            DwollaFundingSourceV1.objects.get_or_create(**receive_only_fs_data)

            # create dwolla business accounts
            business_customer_data = {
                "company": com,
                "external_admin": external_admin,
                "customer_type": DwollaAccountType.BUSINESS,
                "customer_id": "ea5e62a0-8510-4e30-856a-fac75ba8e974",
                "firstName": "{}-BUSS".format(com.name),
                "lastName": "sandbox",
                "email": "dealeradmin_buss@gmail.com",
                "businessName": "{}-BUSS".format(com.name),
                "status": "verified",
                "customer_of": DwollaCustomerOf.ADMIN,
                "address1": "bahria",
                "city": "isb",
                "state": "isb",
                "postalCode": "10001",
                "dateOfBirth": "1965-01-31",
                "social_security_number": "6789",
                "employer_identification_number": "00-0000000",
                }
            business_customer, created = DwollaCustomer.objects.get_or_create(**business_customer_data)

            business_fs_data = {
                "nick_name": "{}-BUSS".format(com.name),
                "name": "{}-BUSS".format(com.name),
                "dwolla_customer": business_customer,
                "customer_fs_id": "a92ffc22-c9f5-483b-a636-d535b51cad7f",
                "routingNumber": "1111112121",
                "accountNumber": "121212121",
                "accountType": "Checking",
                "status": "verified",
                }
            DwollaFundingSourceV1.objects.get_or_create(**business_fs_data)

    def remove_all_dwolla_fk():
        ExternalAdministrator.objects.all().update(
            dwolla_sending_account_name='',
            dwolla_sending_account='',
            dwolla_receiving_account_name='',
            dwolla_receiving_account='',
        )

        DwollaOtherAccount.objects.all().delete()
        LithicPayingClaimAccount.objects.all().delete()

        Dealer.objects.all().update(
            stripe_customer_id='',
            dwolla_customer_id='',
            dwolla_customer_fs_id='',

            dwolla_customer_account=None,
            dwolla_funding_source=None,

            enable_lightspeed=False,
            lightspeed_username='',
            lightspeed_password='',
            lightspeed_CMF='',
            lightspeed_dealership_name=''
        )

        Underwriter.objects.all().update(
            dwolla_customer_id='',
            dwolla_customer_fs_id='',

            dwolla_customer_account=None,
            dwolla_funding_source=None,
        )

        ReInsurance.objects.all().update(
            dwolla_customer_id='',
            dwolla_customer_fs_id='',

            dwolla_customer_account=None,
            dwolla_funding_source=None,
        )

        Member.objects.all().update(
            dwolla_customer_id='',
            dwolla_customer_fs_id='',

            dwolla_customer_account=None,
            dwolla_funding_source=None,
        )

    def change_payable_keys():
        company_obj = Company.objects.all()
        for com in company_obj:
            dealer_obj = Dealer.objects.filter(company__id=com.id)
            business_fs = DwollaFundingSourceV1.objects.filter(dwolla_customer__company__id=com.id, dwolla_customer__customer_type=DwollaAccountType.BUSINESS, name__icontains='BUSS').first()
            ro_fs = DwollaFundingSourceV1.objects.filter(dwolla_customer__company__id=com.id, dwolla_customer__customer_type=DwollaAccountType.RECEIVE_ONLY).first()
            for dealer in dealer_obj:
                if dealer.payment_method == PAYMENTMETHODCHOICES.STRIPE:
                    dealer.stripe_customer_id = 'cus_JVVDbiheRb5nIq'
                else:
                    dealer.dwolla_customer_account = business_fs.dwolla_customer
                    dealer.dwolla_funding_source = business_fs
                dealer.save()

            members = Member.objects.filter(company__id=com.id, enable_payment=True)
            for member in members:
                member.enable_payment = True
                member.w9_received = True
                member.dwolla_account_type = DwollaAccountType.RECEIVE_ONLY
                member.dwolla_customer_account = ro_fs.dwolla_customer
                member.dwolla_funding_source = ro_fs
                member.save()

            underwriters = Underwriter.objects.filter(company__id=com.id)
            for underwriter in underwriters:
                underwriter.dwolla_account_type = DwollaAccountType.RECEIVE_ONLY
                underwriter.dwolla_customer_account = ro_fs.dwolla_customer
                underwriter.dwolla_funding_source = ro_fs
                underwriter.save()

            reinsurances = ReInsurance.objects.filter(company__id=com.id)
            for reinsurance in reinsurances:
                reinsurance.dwolla_account_type = DwollaAccountType.RECEIVE_ONLY
                reinsurance.dwolla_customer_account = ro_fs.dwolla_customer
                reinsurance.dwolla_funding_source = ro_fs
                reinsurance.save()


change_prod_data = ChangeProdData
change_prod_data.change_keys()
change_prod_data.delete_and_create_dummy_dwolla_accounts()
change_prod_data.remove_all_dwolla_fk()
change_prod_data.change_payable_keys()