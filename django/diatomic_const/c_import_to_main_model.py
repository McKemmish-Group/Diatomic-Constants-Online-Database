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
equilibrium_types=[]
for i in constant_source:
    if "e" in i.symbol:
        equilibrium_types.append(i)



######### Now extract the list of syymetries to know their order #########
symm_in_db=Electronic_symmetry.objects.all()
symm_list=['Sigma+','Sigma-','Pi','Delta','Phi','Gamma']
symm_dict={}

counter=0
for i in symm_in_db:
    key=symm_list[counter]
    value=i
    symm_dict[key]=value
    counter+=1


import unicodedata
data=np.load('data.npy').item()
molecules_names_list=np.load('molecules_names_list.npy')


paper_list=Reference_publication.objects.filter(reference_publication_tag="Huber_Herzberg")

paper_object=paper_list[0]


for molecule in molecules_names_list:


    # Statement to skip homonuclear molecules
    if "2" in molecule:
        continue

    if molecule == "CoH":
        continue
    
    if bool(data[molecule])==False:
        continue

    else:
        # Extract inner_dictionary by using molecule name
        inner=data[molecule]
         

        # Iterate over states.
        for state_string, dummy in inner.items():
            cl1=Molecular_state()
            # Make if statesments to accept or
            # skip the state
            state_string=str(state_string) 
            
            # a) Symbol types 1.
            symbols_1=['1g','1u','0g','0u','0u-','0u+','0+','0-']
            
            continue_1=False 
            for i in symbols_1:
                if i in state_string:
                    continue_1=True
                    break
           

            if continue_1==True:
                continue

            symmetry_names=[    'Sigma+',
                                'Sigma-',
                                'Pi',
                                'Delta',
                                'Phi',
                                'Gamma' ]
            

            # b) Find symmetry name
            symmetry_name=""
            for i in symmetry_names:
                if i in state_string:
                    symmetry_name=i
                    break

            # c) Symbol types 2. They come right after state name
            symbols_2=['r', 'i','u','g','u','o-']
            
            continue_2=False
            for i in symbols_2:
                if symmetry_name+i in state_string:
                    continue_2=True
                    break
            
            if continue_2==True:
                continue

            

            # d) Extra symbols to exclude
            symbols_3=['1s','2s','2p',
                       '3p','3s','3d',
                       '4s','4d','4p',
                       '5p','6p',
                       'sigma','delta','DeltaI','Pip','PiI']

            continue_3=False
            for i in symbols_3:
                if i in state_string:
                    continue_3=True
            if continue_3==True:
                continue

            # e) check if ( and ) are in state label
            if "(" and ")" in state_string:
                continue
            
            elif "or" in state_string:
                continue
            
            

            # f) Find total spin after first "_"
            index_of_=state_string.find("_")
            spin_index=index_of_+1
            spin_string=state_string[spin_index]
            spin_int=int(spin_string)
            
            # g) Find excitation index of the state
            start=0
            end=index_of_
            excitation_index=state_string[start:end]
            


            # h) Work with projected_angular_momentum, if it exists.

            pam=""
            found=False
            list_string_1=['1/2','3/2','5/2','7/2','9/2']
            list_float_1=[0.5 , 1.5, 2.5, 3.5, 4.5]

            for i in list_string_1:
                if i in state_string:
                    found=True
                    idx=list_string_1.index(i)
                    pam=list_float_1[idx]
                    break
            

            if found==False:
                candidate=state_string[-1]

                try:
                    pam=int(candidate)
                    if pam == 0:
                        pam=None
                    
                except:
                    pam=None

            
            # i) Now make each instance for the molecular state model
            name0=molecule+"_"+state_string+"_"+"Hub_Herz"
            symbol0=molecule
            excitation_index0=excitation_index
            electronic_symmetry0=symm_dict[symmetry_name] 
            total_electronic_spin0=spin_int
            projected_angular_momentum0=pam
            
           
            cl1.name=name0
            cl1.symbol=symbol0
            cl1.excitation_index=excitation_index0
            cl1.electronic_symmetry=electronic_symmetry0
            cl1.total_electronic_spin=total_electronic_spin0
            cl1.projected_angular_momentum=projected_angular_momentum0 
            cl1.save()            
            
            # j) Work with cosntants list.
            constants=inner[state_string]
            
            counter=-1
             
            for const in constants:
                counter+=1
                type_const=equilibrium_types[counter]
                state=Molecular_state.objects.filter(name=name0)
                state=state[0] 
                cl2=Diatomic_constant() 
                
                exclude=['(',')','[',']','H',
                         'Z','Q','R','<','>',
                         'i','~']
                
                skip=False
                for i in exclude:
                    if i in const:
                        skip=True
                        break
                
                if skip==True:
                    continue
                
                if const==u'\u0412':
                    continue
                try:
                    cl2.molecular_state=state
                    cl2.reference_publication=paper_object
                    cl2.constant_type=type_const
                    cl2.value=float(const)
                    cl2.save() 
                except:
                       pass
               
              
             
            
           










 
