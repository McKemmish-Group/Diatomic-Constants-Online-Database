# THis code is used to add data to the database.
# It can also be used later for adding more data


##### To run this file symply use the command in terminal ##############
        
    #######   python import.py ##########

##### Setup lines of code so django and models will work ################

import csv,sys,os
import numpy as np
project_dir="/srv/www/diatomic_const/diatomic_const"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE']='settings'

import django


django.setup()
#basically we just added project settings file so we can edit models of database ######
######################### end of setup lines ##############################



################### Test django and models ################################
'''
from data_management.models import *

data=Diatomic_constant.objects.all()

for i in data:
    print(i)
'''
######################## end of test ######################################



#################### Test of addition of dummy paper ###############################
#################### to the reference_publication model ############################
'''
from data_management.models import *

a=Reference_publication()
a.reference_publication_tag="test_paper"
a.entry_type="test_paper"
a.author="test"
a.title="test"
a.journal="test"
a.year=2019
a.volume=2019
a.pages="2019"
a.save()
'''

################## test is successful ################################################
### if you run upper lines, in reference_publication model test_paper will appear ####
################### end of test ######################################################






######################### 




################ create list of e_constants that are in this database #######
from data_management.models import *
constant_source=Constant_type.objects.all()



########## Make list of equilibrium types constants ######################
equilibrium_types=[]
for i in constant_source:
    if "e" in i.symbol:
        equilibrium_types.append(i)



data_to_add=np.load('data.npy').item()
molecules_names_list=np.load('molecules_names_list.npy')


counter=0

#symbol=molecules_names_list[0]

for symbol in molecules_names_list:
    inner=data_to_add[symbol]

    
    for state, dummy in inner.items():
        constants=inner[state]


        count=-1
        for constant in constants:
            count+=1

            skip=True
            for i in constant:
                if i.isdigit()==True:
                    skip=False
                    break

            if skip==True:
                continue

            cl=New_data()
     
            const_type=equilibrium_types[count]
            cl.symbol=symbol
            cl.state=state
            cl.value=constant
    
            if "[" and "]" in constant:
                cl.alternate_type=True
   
            
            


            if "H" in constant:
                cl.source_type="experiment band head"
            elif "Z" in constant:
                cl.source_type="experiment band origin"
            else:
                cl.source_type="experiment"
 

            if "(" and ")" in constant:
                cl.is_uncertain=True
    
            cl.constant_type=const_type
    

            if ">" in constant:
                cl.extra_symbol=">"

            elif "<" in constant:
                cl.extra_symbol="<"
    
            cl.save()
    




 



