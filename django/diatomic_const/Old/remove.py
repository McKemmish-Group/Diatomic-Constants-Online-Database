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

#######################################################
from data_management.models import New_data

all_data=New_data.objects.all()

all_data.delete()



















