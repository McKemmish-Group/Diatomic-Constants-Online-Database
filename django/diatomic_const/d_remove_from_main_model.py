#### THis file is to remove all data from a certain model

#### in this particular case to delete from New_data model





####### setup lines ############

import csv, sys, os
import numpy as np
project_dir="/srv/www/diatomic_const/diatomic_const"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='settings'

import django

django.setup()

############## Deleting data from New_data model ##################
'''
from data_management.models import New_data

all_data=New_data.objects.all()

all_data.delete()
'''
#####################################################################



from data_management.models import *

############ Before deleting states, you need to delete Diatomic_constant###
data=Diatomic_constant.objects.all()
for i in data:
    if i.reference_publication.reference_publication_tag=="Huber_Herzberg":
        i.delete()




############ Deleting data from Molecular_states with TEST word in it ####

from data_management.models import Molecular_state
d=Molecular_state.objects.all()

for i in d:
    if "Hub_Herz" in i.name:
        i.delete()

############################################################################


'''
paper_object=Reference_publication.objects.filter(reference_publication_tag="Huber_Herzberg")
paper_object=paper_object[0]

m_state=Molecular_state.objects.filter(name="10BO_X2Sigma+")
m_state=m_state[0]

value=100.001

cons_type=Constant_type.objects.all()
cons_type=cons_type[0]

cl=Diatomic_constant()
cl.molecular_state=m_state
cl.reference_publication=paper_object
cl.constant_type=cons_type
cl.value=value
cl.save()
'''

'''
a=Diatomic_constant.objects.all()
for i in a:
    if i.reference_publication.reference_publication_tag=="Huber_Herzberg":
        
        i.delete()
'''

































