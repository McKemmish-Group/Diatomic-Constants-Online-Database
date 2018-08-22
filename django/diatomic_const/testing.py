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



d=Diatomic_constant.objects.all()
print(d[1])




