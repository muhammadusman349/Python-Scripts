import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()


from retailer.models import MiscOverfundDistributionAgreement

misc_overfund_id = 2141
member_of = "Admin"
member_id = 1290
underwriter = ""

misc_overfund = MiscOverfundDistributionAgreement.objects.filter(id=misc_overfund_id).update(member_of=member_of, member=member_id, underwriter=underwriter)