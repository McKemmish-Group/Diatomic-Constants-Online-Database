# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from data_management.models import *
from django.template.defaulttags import register

from django.db.models import Q



    

################################# BLOCK 1 #####################################
# This block with the following scheme:
# Molecules_list/Molecule/Paper_name

# FUNCTION 1. 
# THis function produces the list of unique molecules.
# Excluding isotopologs with numbers.

def unique_molecules(request):
    with_numbers=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    without_numbers=[]
    for string in with_numbers:
        # FIrst check the number if capital letters
        # If number is 1, and it has number 2; then it is homonuclear
        
        count=0
        for letter in string:
            if letter.isupper() == True:
                count+=1

        if count==1:
            without_numbers.append(string)        
        
        else:

            result=''.join([i for i in string if not i.isdigit()])
            without_numbers.append(result)
    
    without_numbers=set(without_numbers)
    without_numbers=sorted(without_numbers)
    variables={'molecules_list':without_numbers}
    return render(request, 'filter/a_molecules_list.html', variables)
    




# FUNCTION 2.
# This function produces table of isotopologs, states, and constants
# The sections names a,b,c,d,... is following the the pseudo code from 
# the main report in section 3.2.2 

def table_for_molecule(request,molecule_name):
   
    # a)
    # Make list of e_constants types
    constant_source=Constant_type.objects.all()
    equilibrium_types=[]
    for i in constant_source:
        if "e" in i.symbol and "H" not in i.symbol:
            equilibrium_types.append(i)



    
    # b)
    data=Molecular_state.objects.all()
    
    states_list=[]
    for state in data:
        name_with_numbers=state.symbol
        
        
        # Seperate homonuclear molecules
        count=0
        for letter in name_with_numbers:
            if letter.isupper() ==True:
                count+=1
        
        if count==1:
            no_numbers=name_with_numbers
        
        else:
            no_numbers=''.join([i for i in name_with_numbers if not i.isdigit()])
        
        if str(no_numbers) == str(molecule_name):
            states_list.append(state)
    
    #c)
    # Now find all isotopologs. Even if there is only one
    isotopologs=[]

    for entry in states_list:
        name=entry.symbol
        if name not in isotopologs:
            isotopologs.append(name)
    isotopologs=sorted(isotopologs)


    #d)
    # FOr each isotopolog find the list of states
    main={}
    for isotopolog in isotopologs:
        d1={}
        states_of_isotopolog=[]
        for state in states_list:
            if state.symbol==isotopolog:
                states_of_isotopolog.append(state)
    

        # e)
        # FOr each of the state, find ALL constans
        for state in states_of_isotopolog:
            inner={}
            all_constants_of_state=Diatomic_constant.objects.filter(molecular_state=state)
            

            # f) 
            # Filter those with 'e' them
            e_constants=[]
            for const in all_constants_of_state:
                if "e" in const.constant_type.symbol and "H" not in const.constant_type.symbol:
                    e_constants.append(const)
                    # For now we need to remove H_e constant from the previous list
                

            # Now e_constants list must be sorted according to order of equilibrium_types
            sorted_e_constants=[]
            for const_th in equilibrium_types:
                for const in e_constants:
                    if const_th.symbol==const.constant_type.symbol:
                        sorted_e_constants.append(const)

            # g) First find unique_papers and make list
            unique_papers=[]
            for entry in sorted_e_constants:
                if entry.reference_publication.reference_publication_tag not in unique_papers:
                    unique_papers.append(str(entry.reference_publication.reference_publication_tag))
            
            # h) Find constants for each paper and put into list for each paper
            #    Then isert into new dicrionary
            ############### NEW ATTEMPT ##############################################
            papers_and_values={}
            for paper in unique_papers:
                all_const_of_paper={}
                for e_type in equilibrium_types:
                    the_list=[]
                    for const in sorted_e_constants:
                        if const.reference_publication.reference_publication_tag==paper:
                            if const.constant_type.symbol==e_type.symbol:
                                the_list.append(const)
                        all_const_of_paper[str(e_type)]=the_list

                papers_and_values[str(paper)]=all_const_of_paper
                    

            ###########################################################################
         
            # i)
            #inner[str("constants")]=sorted_constants
            inner[str("state_object")]=state
            inner[str("ordered_papers")]=unique_papers  
            inner[str("papers_and_values")]=papers_and_values        
            

            # Here is the difference.
            # ROWSPAN must be the number of unique papers, but
            # not the number of available constants

            number_of_papers=len(unique_papers)
            if number_of_papers==0:
                remaining=0 
                rowspan=1
            else:
                remaining=number_of_papers-1
                rowspan=number_of_papers
            inner[str("rowspan")]=rowspan
            inner[str("remaining")]=remaining
            # g)
            d1[str(state)]=inner
       
        # k) 
        main[isotopolog]=d1
        
    


    # Prepare descriptions for each symbol in equilibrium_types#
    # This is because in HTML for loop is used, hence we need
    # to preliminarily prepare them
    
    descriptions=[ 
                    "Minimum electronic energy" ,
                    "internuclear distance ",
                    "rotational constant in equilibrium position ",
                    "vibrational constant - first term ",
                    "vibrational constant - second term ",
                    "vibrational constant - third term ",
                    "rotational constant - first term  ",
                    "rotational constant - first term, centrifugal force",
                    "rotation-vibration interaction constant",
                    "centrifugal distortion constant",
                     
                ]
      
    symbols_dictionary={}
    counter=0
    for symbol in equilibrium_types:
        symbols_dictionary[str(symbol)]=descriptions[counter]
        counter+=1

    
    variables={'states':states_list,
               'name':molecule_name,
               'isotopologs':isotopologs,
               'main':main,
               'equilibrium_types':equilibrium_types,
               'symbols_dictionary':symbols_dictionary}
                                
    return render(request, 'filter/d_molecule_states_table.html',variables)
    
  
# FUNCTION 3. 
# This function shows the info about specific paper for specific ISOTOPOLOG

def paper_info(request, isotopolog, paper):
    paper_object=Reference_publication.objects.filter(reference_publication_tag=paper)    

  
    # Now let's find all states and constants mentioned in this paper
    # a) All constants
    all_constants=Diatomic_constant.objects.all()
    
    # b) Loop over all constants and find those with given paper
    constants_of_paper=[]
    for entry in all_constants:
       
        if entry.reference_publication.reference_publication_tag == paper:
            constants_of_paper.append(entry)
        
    # c) Find number of constants for this paper
    number_of_constants=len(constants_of_paper) 

    # d) Find number of states mentioned in this paper
    states_of_paper=[]
    for entry in all_constants:
        if entry.reference_publication.reference_publication_tag == paper:
            if entry.molecular_state not in states_of_paper:
                states_of_paper.append(entry.molecular_state)

    number_of_states=len(states_of_paper)

    variables={ 'paper_object':paper_object[0],
                'paper_name':paper,
              # 'constants_of_paper':constants_of_paper
                'number_of_constants':number_of_constants,
                'number_of_states':number_of_states
              } 




    return render(request, 'filter/e_paper_info.html', variables)







# FUNCTION 4. This is the copy of function 2 that collects info
# for a single molecule. THis function is a simple python function.
# It will be used in the next function to be  repeatedly used in for loop.

def info_for_molecule(molecule_name):
    # Make list of e_constants types
    constant_source=Constant_type.objects.all()
    equilibrium_types=[]
    for i in constant_source:
        if "e" in i.symbol and "H" not in i.symbol:
            equilibrium_types.append(i)




    data=Molecular_state.objects.all()
    
    states_list=[]
    for state in data:
        name_with_numbers=state.symbol
        
        
        # Seperate homonuclear molecules
        count=0
        for letter in name_with_numbers:
            if letter.isupper() ==True:
                count+=1
        
        if count==1:
            no_numbers=name_with_numbers
        
        else:
            no_numbers=''.join([i for i in name_with_numbers if not i.isdigit()])
        
        if str(no_numbers) == str(molecule_name):
            states_list.append(state)
    
    # Now find all isotopologs. Even if there is only one
    isotopologs=[]

    for entry in states_list:
        name=entry.symbol
        if name not in isotopologs:
            isotopologs.append(name)
    isotopologs=sorted(isotopologs)

    # FOr each isotopolog find the list of states
    main={}
    for isotopolog in isotopologs:
        d1={}
        states_of_isotopolog=[]
        for state in states_list:
            if state.symbol==isotopolog:
                states_of_isotopolog.append(state)
    
        # FOr each of the state, find ALL constans
        for state in states_of_isotopolog:
            inner={}
            all_constants_of_state=Diatomic_constant.objects.filter(molecular_state=state)
            
            # Filter those with 'e' them
            e_constants=[]
            for const in all_constants_of_state:
                if "e" in const.constant_type.symbol and "H" not in const.constant_type.symbol:
                    e_constants.append(const)
            

            # Now e_constants list must be sorted according to order of equilibrium_types
            sorted_e_constants=[]
            for const_th in equilibrium_types:
                for const in e_constants:
                    if const_th.symbol==const.constant_type.symbol:
                        sorted_e_constants.append(const)

            # a) First find unique_papers and make list
            unique_papers=[]
            for entry in sorted_e_constants:
                if entry.reference_publication.reference_publication_tag not in unique_papers:
                    unique_papers.append(str(entry.reference_publication.reference_publication_tag))
            
            # b) Find constants for each paper and put into list for each paper
            ############### NEW ATTEMPT ##############################################
            papers_and_values={}
            for paper in unique_papers:
                all_const_of_paper={}
                for e_type in equilibrium_types:
                    the_list=[]
                    for const in sorted_e_constants:
                        if const.reference_publication.reference_publication_tag==paper:
                            if const.constant_type.symbol==e_type.symbol:
                                the_list.append(const)
                        all_const_of_paper[str(e_type)]=the_list

                papers_and_values[str(paper)]=all_const_of_paper
                    

            ###########################################################################
 

            
            inner[str("state_object")]=state
            inner[str("ordered_papers")]=unique_papers  
            inner[str("papers_and_values")]=papers_and_values        
            

            # Here is the difference.
            # ROWSPAN must be the number of unique papers, but
            # not the number of available constants

            number_of_papers=len(unique_papers)
            if number_of_papers==0:
                remaining=0 
                rowspan=1
            else:
                remaining=number_of_papers-1
                rowspan=number_of_papers
            inner[str("rowspan")]=rowspan
            inner[str("remaining")]=remaining
            d1[str(state)]=inner
        
        main[isotopolog]=d1
        main[str("isotopologs_list")]=isotopologs    
    
    
    
   
                                
    return main
    
 




# FUNCTION 5. This function uses function_4 to build big table.

def large_table(request):
    # Make list of unique_molecules
    with_numbers=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    without_numbers=[]
    for string in with_numbers:
        count=0
        for letter in string:
            if letter.isupper()==True:
                count+=1
        if count==1:
            without_numbers.append(string)
        else:
            result=''.join([i for i in string if not i.isdigit()])
            without_numbers.append(result)

    without_numbers=set(without_numbers)
    without_numbers=sorted(without_numbers)
    

    # Make equilibrium types
    constant_source=Constant_type.objects.all()
    equilibrium_types=[]
    for i in constant_source:
        if "e" in i.symbol and "H" not in i.symbol:
            equilibrium_types.append(i)


    main0={}
    for molecule_name in without_numbers:
        inner=info_for_molecule(molecule_name)
       
        main0[str(molecule_name)]=inner 


    
    descriptions=[ 
                    "Minimum electronic energy" ,
                    "internuclear distance ",
                    "rotational constant in equilibrium position ",
                    "vibrational constant - first term ",
                    "vibrational constant - second term ",
                    "vibrational constant - third term ",
                    "rotational constant - first term  ",
                    "rotational constant - first term, centrifugal force",
                    "rotation-vibration interaction constant",
                    "centrifugal distortion constant",
                    
                ]
      
    symbols_dictionary={}
    counter=0
    for symbol in equilibrium_types:
        symbols_dictionary[str(symbol)]=descriptions[counter]
        counter+=1


    
    variables={'equilibrium_types':equilibrium_types,
               'molecules_names_list':without_numbers,
               'main0':main0,
               'symbols_dictionary':symbols_dictionary
              }

    return render(request,'filter/f_big_table.html', variables)
    









############## BLOCK 2 . Data from HH database. Comparing with main ############

#### FUNCTION 6. This function just makes the list of the molecules from HH database ##################

def molecules_from_HH(request):
    import numpy as np
    molecule_names_list=np.load("/srv/www/diatomic_const/molecules_names_list.npy")
    
    variables={'molecules_from_HH':molecule_names_list} 
    return render(request, 'filter/g_list_from_HH.html',variables )

##############################################################################







### FUNCTION 7. This function produces the simple table to see what data was entered and what not ####

def compare_table(request, name):
    # find constants based on name
    selected=New_data.objects.filter(symbol=name)    
    
    # make equlibrium_types list
    constants_source=Constant_type.objects.all()
    equilibrium_types=[]
    for i in constants_source:
        if "e" in i.symbol and "H" not in i.symbol:
            equilibrium_types.append(i)
    
    # Find all unique_states
    unique_states=[]
    for i in selected:
        if i.state not in unique_states:
            unique_states.append(i.state)

    
    #for each states find sorted constants
    inner={}
    for state in unique_states:
        #first find all relevant constants
        relevant=[]
        for i in selected:
            if i.state==state:
                relevant.append(i)


        inner[str(state)]=relevant

    variables={'name':name,
               'inner':inner,
               'states':unique_states,
               'states_number':len(unique_states) }

    return render(request,'filter/h_compare_table.html', variables )






