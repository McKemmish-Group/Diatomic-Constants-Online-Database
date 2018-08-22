# This code imports Huber_Herzberg database into New_data model.
# This model is not main model. It was made to keep track on what data
# was already moved to main database

######### Setup lines ##################
import csv,sys, os
import numpy as np
project_dir="/srv/www/diatomic_const/diatomic_const"
sys.path.append(project_dir)
os.environ["DJANGO_SETTINGS_MODULE"]='settings'
import django
django.setup()
########################################

from data_management.models import *

constant_source=Constant_type.objects.all()
equilibrium_types=[]
for i in constant_source:
    if "e" in i.symbol:
        equilibrium_types.append(i)


data_to_add=np.load('data.npy').item()
molecules_names_list=np.load('molecules_names_list.npy')
counter=0


orbyts_states=Molecular_state.objects.all()
orbyts_constants=Diatomic_constant.objects.all()

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
                cl.source_type="experement band origin"
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
            
         
        
            



