# FUnctions
from __future__ import unicode_literals
from django.db import models
from data_management.models import Molecular_state,Reference_publication,Diatomic_constant,Preferred_set,Constant_type,Electronic_symmetry


from django.db.models import Q

# THis file makes list of all molecule types are here and types of constants
# Meaning: "cl.molecular_state.symbol"
# Meaning: "cl.const_type.symbol."
# Here: cl is all data from database

# Function 1. To print all molecules by using only Molecular State model

def fun_1():
    print(" ")
    print("Molecules by only Molecular State")
    data=Molecular_state.objects.all()
    all_molecules=[]
    for i in data:
        molecule=i.symbol
        if molecule not in all_molecules:
            all_molecules.append(molecule)
    
    all_molecules.sort()
    count=1
    for i in all_molecules:
        print count, " ", i
        count+=1        
    print(" ")


# FUnction 2. To print all molecules by using Diatomic_constant.molecular state model

def fun_2():
    print(" ")
    print("By Diatomic constant")
    all_data=Diatomic_constant.objects.all()
    all_molecules=[]

    for i in all_data:
        molecule=i.molecular_state.symbol
        if molecule not in all_molecules:
            all_molecules.append(molecule)
    
    all_molecules.sort()
    c=1
    for i in all_molecules:
        print c," ",i
        c+=1
    print(" ")

# Function 3. What is ELECTRONIC SYMMETRY?
# THis just gives list of capital: s,p,d,f,g
def excitation_index():
    data=Electronic_symmetry.objects.all()
    for i in data:
        print(i.reflection_symmetry)


# FUnction 4. Everything in Molecular state model
def all_molecular_state():
    print(' ')
    print("Everything in Molecular state model")
    data=Molecular_state.objects.all()
    for i in data:
        print(i)

# FUnction 5. Similar as Function 4, but now each entry is parsed

def parsed_molecular_state():
    print(' ')
    print('Parsed in MOlecluar state')
    data=Molecular_state.objects.all()
    for i in data:
        name=i.name
        symbol=i.symbol
        excitation_index=i.excitation_index
        sym=i.electronic_symmetry
        el_spin=i.total_electronic_spin
        ang_mom=i.total_angular_momentum
        proj=i.projected_angular_momentum
        refl=i.reflection_symmetry
        parity=i.parity
        
        print name,' ',symbol,' ',excitation_index,' ',sym,' ',el_spin,' ',ang_mom,' ',proj,' ',refl,' ',parity



# FUnction 6. Testing Constant_type model


def constant_type():
    data=Constant_type.objects.all()
    for i in data:
        print(i)





# FUnction 7. THis is TEST function. Prints all instances from 
# molecular_state

def all_values(name):
    data=Diatomic_constant.objects.all()
    values=[]
    for i in data:
        if i.molecular_state.symbol==name:
            values.append(i)
    
    a=values[30]
    print(a.molecular_state)
    print(a.molecular_state.parity)
    print(a.molecular_state.projected_angular_momentum) 



# FUnction 8. This function prints out all types of constant in one list

def constant_types():
    data=Constant_type.objects.all()
    print("There are ",len(data)," constants")
    
    selected=[] 
    for i in data:
        if "e"in i.symbol:
            selected.append(i)
    
    for i in selected:
        print(i) 








    


# Printing molecules actual names
def names():
    data=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    data=sorted(data)
    count=1
    for i in data:
        print(count," ",i)
        count+=1






# function to debug BO molecule
def debug_1():
    states=Molecular_state.objects.filter(Q(symbol="10BO")| Q(symbol="11BO"))
    
    for state in states:
        data=Diatomic_constant.objects.filter(molecular_state=state)     
    
        print("For ",state," constants are")
        for const in data:
            print(const.constant_type)
        print(" ")     




# Function to find all UNIQUE molecules. Excluding isotopologs.

def unique_molecules():
    with_numbers=Molecular_state.objects.values_list('symbol',flat=True).distinct()
    without_numbers=[]
    for string in with_numbers:
        result=''.join([i for i in string if not i.isdigit()])   
        without_numbers.append(result)
    without_numbers=set(without_numbers)
    for i in without_numbers:
        print(i)


     


    
    






























