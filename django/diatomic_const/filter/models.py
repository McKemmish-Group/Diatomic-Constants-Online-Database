# FUnctions
from __future__ import unicode_literals
from django.db import models
from data_management.models import Molecular_state,Reference_publication,Diatomic_constant,Preferred_set,Constant_type


# THis file makes list of all molecule types are here and types of constants
# Meaning: "cl.molecular_state.symbol"
# Meaning: "cl.const_type.symbol."
# Here: cl is all data from database

def fun(printing=False):
    # Select everything from database
    all_data=Diatomic_constant.objects.all()

    #Prepare list for symbol
    molecules_list=[]
    #list for constant types
    const_types=[]
    for sample in all_data:
        # Get all symbols of molecules
        sym=sample.molecular_state.symbol
        if sym not in molecules_list:
            molecules_list.append(sym)
        # Get the all constant types in database
        a1=sample.constant_type.symbol
        if a1 not in const_types:
            const_types.append(a1)

    if printing==True:
        print "There are ",len(molecules_list)," molecules types in database"
        print "There are ",len(const_types)," types of constants"
    return molecules_list,const_types

