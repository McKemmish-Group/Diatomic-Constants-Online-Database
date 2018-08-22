This is a simple guide related to this project.
It is implemented in question-answer format.




Q: What would you suggest for django learning?

A: For beginning I used simple youtube videos.
    There are good playlists there. However, there is no need to completely
    watch all videos. A little bit of introduction is enough, but then it is better to
    learn something specific that is needed for the website.

Q:  I am working on the project remotely. Meaning, I access the source code via linux terminal.
    How do i create simple python code that uses current data and prints it on the screen?

A:  There are 2 ways of doing it. 
    
    First way. Create some file with Python code. You can add commands like:
    
    data_management.models import *
    data=Diatomic_constat.objects.all()
    for i in data:
        print(i) 
    
    If you try to run the script in standard way :  python file.py , it will not work.
    You need to go "django python shell".
    
    Go to a folder where manage.py file is located and run:  python manage.py shell
    This command will move you to the python where you can code simple Python.
    Make sure that your file.py is located in the same folder as manage.py.
    Then in python shell you can use command:  execfile('file.py')
    This command will execute the code above and print everything.
    If your file.py is not in same folder as manage.py, you will have to use 
    import os and use changing directory commands and etc.



    Second way. This way allows you to use simple standart command without going to django python shell.
    However, you will need to add more lines of code. If you open any python file in the main project folder,
    you will see some setup lines. For example, you can open a_new_data_model.py file and see the lines there.




Q:  I need to copy some files from my local machine to the project folder. However, the project folder
    is located on some server which is on campus.

A:  There is concept called copy files from local machine to remote machine. If you are not familiar with it,
    simply search online: how to copy files from local to remote machine? how to use scp command to copy between
    local and remote machine? 
    The google will return very good examples. Youtube has good videos as well



Q:  If i want to copy 100 files, should i use the scp commands 100 times?
    
A:  No. You can just make tar.gz archive in terminal. If needed, you can simply add the whole folder to archive,
    and then you can copy it as only 1 file. 



Q: What if i want to declare variables in html? How do i that?

A: There are several options of doing it. Some of the were complicated for me, so i used the simplest

    In django template you can use tag {%with%} 
    
    Example:
    
    {%with banana = 10 %}
        
        <p> {{banana}} </p>   # So here in paragraph number 10 will appear
    {%endwith%}      

    The banana variable will work only in this block, after using endwith, it will not work.
    This is the simples way of declaring variables.




Q: If i pass dictinonary from view function, how do i access it within django template?

A: If the dictionary is NOT nested, it is done with dot lookup. 
    Example:
    Let's say the name of the dictionary is: dict.
    In django template
    
    <p> {{dict.key}} </p>  

    This will just print the value of the key.


    However, if the dictionary is nested, then intuitive double, tiple dot lookup will not work

    <p> {{dict.key1.key2.key3}} </p> 
    
    This will not work

    To solve this problem, we use django custom filters. For this project there is one exmample in
    templatetags folder in filter app.
    
    Then, you can see that almost all html templates uses this line {% load dictionary_lookup %}
    This line loads our filters from the templatetags.
    
    Also, almost all templates in filter app uses a lot of {%with%} tags. 
    This is because I assigned simple name for each inner dictionary. 


Q: I try to lookup a dictionary, but something does not work

A: There may be problem with datatypes. For simplicity, I made all dictionary keys as strings in Python view functions.
    Then in html it was easier to access them. Try to make all keys as strings, then maybe it will work as well.
    There also can be problem with str and unicode type. Sometimes the string is not string but unicode format.
    This caused me initial problems initially. Hence, I had to change unicode to strings and then everything worked.







Q: I edited the model for my project, removed some fields , added some fields, but it does not work.
    Like no changes were made.


A: Any time when you change source code of the models in models.py, you need to use these commands in the terminal.
   
    python manage.py makemigrations
    python manage.py migrate






Q: I made new model in my django models.py, but it does not show up in the admin interface. Like it 
    does not exist yet.


A: After the new model is created, it has to be registered in the admin.py. 
    Go to the app where the new model was created. Inside the app folder there
    is admin.py  file. For example, in data_management folder, admin.py. 
    you can see the names of all models. If the name of the new model is not
    there, then the model is not yet registered. After creating new model,
    dont forget to use 2 commands explained above.





Q: I edit view function, but the changes are not applied.

A: After editing views, urls , models files, you need to restart gunicorn
    by the command : sudo service gunicorn restart
    THen it will ask for you password.


