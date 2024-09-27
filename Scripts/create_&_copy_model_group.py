import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from company.models import ModelGroup
from copy import deepcopy
from django.db import transaction

'''
can you create a new model Group "OnRoad ALL(No Sling|3wheel) 
Copy it from the On Road All and just delete CanAm Powersports and Sling?

'''

model_id  = 6
new_name = "RV ALL(No Sling|3wheel)"
model = ModelGroup.objects.get(id = model_id)
with transaction.atomic():
    new_model = deepcopy(model)
    new_model.id = None
    new_model.name =new_name
    new_model.save()

    new_model.subplan_model.set(model.subplan_model.all())

