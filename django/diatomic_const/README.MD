This is a short instruction regarding the written code for the
masters project, 2017-2018.


1) The oringinal source code is located in the "data_management" app.

2) My personal contributions are located in the "filter" app, and in some
   scripts saved in the root folder of this project.

3) The source code could be tested only by seing results on the website:
   http://octahedron.theory.phys.ucl.ac.uk/login/


Part 1. Filter app.

i)  The app contains standart django main files: models, views, urls. 

    THere are no new written models in the filter.models.py file.
    Instead, filter app imports all models from the data_management.models.py.

    Urls.py contain necessary link names and the respective view functions.

    The views.py file contain all functions that are used in data query.
    This file contains 6 view functions and 1 additional which is used within a view function. 
    The short description for each function is presented.

    FUNCTION 1. Produce the list of molecules in the database
    FUNCTION 2. Produces the table of constants, papers for a selected molecule.
    FUNCTION 3. Details of selected paper.
    FUNCTION 4. Additional function(logic is same as 2). It is used in a loop.
    FUNCTION 5. Produces the large table. Uses function 4 in a loop.
    FUNCTION 6. Molecule names from the Huber-Herzberg database.
    FUNCTION 7. Table to compare which constans and states were imported.

ii) The standart filter app template folder contains 6 html files.
    
    Each file is linked with a view function.
    a_molecules_list.html        - function 1
    d_moelcules_statesTable.html - function 2
    e_paper_info.html            - function 3
    f_big_table.html             - function 5
    g_list_from_HH.html          - function 6
    h_compare_table.html         - function 7

    In addition, the filter app contains templatetags folder. This directory stores custom
    filters written for html tempaltes. In particular, we have added only 1 : dictionary_lookup.py.
    Without this filter, the nested dictionary lookup does not work.

iii) Apart from the main filter app, there are some additional files in the project root folder.
    
    a) data.npy
    This file contains the data,which were proviede in csv format, from Huber-Herzberg database. 
    The file contains one nested dictionary, where key: molecule_name and value: states and constants.
    The constants are sorted in the specific way. The order is as same as it appears in the website.
    This type of ordering is convenient in for loops.
    
    b) molecules_names_list.npy
    This file contains one list of aplhabetically ordered molecules from the provided Huber-Herzberg data/
    The values of the list are used as keys for the dictionary mentioned above.

    c) a_new_data_model.py
    Since currently the models of the database have no option of storing all information about states
    and molecules, additional model was created. It is called New_model. The execution of this file in
    terminal will import ALL data from data.npy into the New_data model. Everything will be store
    as characters. ALL DATA IS ALREADY IN NEW_DATA MODEL. NO NEED TO EXECUTE SCRIPT AGAIN.

    d) b_remove_from_new.py
    If executed in terminal, this script will remove ALL data from New_data model.

    e) c_import_to_main_model.py
    This script will import the suitable NEW states and NEW constants from data.npy into
    Molecular_states and Diatomic_constant models. NO NEED TO EXECUTE BECUASE CONSTANTS ARE ALREADY 
    IMPORTED. If executed, there will be repeating values.
    
    f) d_remove_from_main_model.py
    If necessary, we can remove new states and new constants from Molecular_states and
    Diatomic_constant models.

    g) e_compare_HH.py
    This file modifies data in New_data model. After files a and c are executed, we use this script
    to check is the states and constants were imported. 
    
    Overall, these files could be run anytime to add and remove data.  










































































