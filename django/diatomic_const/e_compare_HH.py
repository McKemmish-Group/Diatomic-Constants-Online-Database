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



from data_management.models import *

def compare_HH():
    # open file with molecules names
    molecule_names_list=np.load("/srv/www/diatomic_const/molecules_names_list.npy")
    # Constants with Huber_Herzberg entry
    with_HH=[]
    all_data=Diatomic_constant.objects.all()
    for i in all_data:
        if i.reference_publication.reference_publication_tag=="Huber_Herzberg":
            with_HH.append(i)
    
    # check if states are imported to main DB
    for molecule in molecule_names_list:
        constants=New_data.objects.filter(symbol=molecule)

        for const in constants:
            state_name=molecule+'_'+const.state+"_Hub_Herz"
            # check if the state in main DB
            state_test_list=Molecular_state.objects.filter(name=state_name)
            if len(state_test_list)!=0:
                const.state_in_orbyts=True
                const.save()

            # check if the constant value in the database
            stop=False
            for entry in with_HH:
                if stop==True:
                    break
        
                if entry.molecular_state.symbol==molecule:
                    float_value=entry.value
                    from_new=const.value
                    try:
                        float_new=float(from_new)
                        if float_new==float_value:
                            const.constant_in_orbyts=True
                            const.save()
                            stop=True
    

                    except:
                        pass




compare_HH()






































