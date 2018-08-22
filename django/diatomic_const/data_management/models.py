# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.

class Electronic_symmetry(models.Model):
    electronic_symmetry_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=200,blank=True, default='')
    reflection_symmetry = models.CharField(max_length=1,blank=True, default='')

    def __unicode__(self):
        return unicode(self.symbol)+unicode(self.reflection_symmetry)

class Molecular_state(models.Model):
    molecular_state_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200) #molecular state description
    symbol = models.CharField(max_length=200) # Molecule name
    excitation_index = models.CharField(max_length=2) #Electronic state label
    electronic_symmetry = models.ForeignKey(Electronic_symmetry, default=0) #electron symmetry (sigma, pi etc)
    total_electronic_spin = models.PositiveIntegerField(default=0) #Electronic spin (2S+1) - 1,2,3,...
    total_angular_momentum = models.IntegerField(blank=True,null=True,default=0)
    projected_angular_momentum = models.DecimalField(blank=True,null=True,decimal_places=1,max_digits=2)
    reflection_symmetry = models.CharField(max_length=1,blank=True, default='')
    parity = models.CharField(max_length=1, blank=True, default='')
    date_entered = models.DateField(auto_now=True)
    user_entered = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    def __unicode__(self):
	#        selfString = self.excitation_index + '^' + unicode(2*self.total_electronic_spin+1) + ' ' + unicode(self.total_angular_momentum) + '_' + unicode(self.projected_angular_momentum) + ',' + self.parity + '^' + self.reflection_symmetry + ' ' + self.symbol
        return unicode(self.name) #selfString

class Reference_publication(models.Model):
    reference_publication_id = models.AutoField(primary_key=True)
    reference_publication_tag = models.CharField(unique=True,max_length=200,blank=True, default='')
    entry_type = models.CharField(max_length=200)
    author = models.CharField(max_length=2000)
    title = models.CharField(max_length=2000)
    journal = models.CharField(max_length=2000)
    year = models.IntegerField()
    volume = models.IntegerField()
    doi = models.CharField(max_length=200,blank=True, default='')
    url = models.CharField(max_length=200, blank=True, default='')
    number = models.CharField(max_length=200, blank=True, default='')
    pages = models.CharField(max_length=200)
    note = models.TextField(blank=True, default='')
    date_entered = models.DateField(auto_now=True)
    user_entered = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    def __unicode__(self):
        return unicode(self.reference_publication_tag) 

class Constant_type(models.Model):
    constant_type_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    date_entered = models.DateField(auto_now=True)
    user_entered = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)    
    def __unicode__(self):
        return self.symbol


class Source_type(models.Model):
    source_type_id = models.AutoField(primary_key=True)
    source_type = models.CharField(max_length=200)
    date_entered = models.DateField(auto_now=True)
    user_entered = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
        
    def __unicode__(self):
        return self.source_type


class Diatomic_constant(models.Model):
    diatomic_constant_id = models.AutoField(primary_key=True)
    molecular_state = models.ForeignKey(Molecular_state, on_delete=models.PROTECT)
    reference_publication = models.ForeignKey(Reference_publication, on_delete=models.PROTECT)
    constant_type = models.ForeignKey(Constant_type, on_delete=models.PROTECT)
    value = models.FloatField()
    delta_plus = models.FloatField(blank=True, default=0)
    delta_minus = models.FloatField(blank=True, default=0)
    source_type = models.ForeignKey(Source_type,default=2)
    date_entered = models.DateField(auto_now=True)
    user_entered = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    def __unicode__(self):
            return unicode(self.reference_publication) + " " + unicode(self.constant_type) + " " + unicode(self.molecular_state) + " " + unicode(self.source_type)



class Preferred_set(models.Model):
    preferred_set_id = models.AutoField(primary_key=True)
    molecular_state = models.OneToOneField(Molecular_state, on_delete=models.PROTECT)
    constant_type = models.OneToOneField(Constant_type, on_delete=models.PROTECT)
    reference_publication_id = models.ForeignKey(Reference_publication, on_delete=models.PROTECT, null=True)
    source_type = models.ForeignKey(Source_type, null=True)
    date_entered = models.DateField(auto_now=True)
    user_entered = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)


    def __unicode__(self):
        return unicode(self.reference_publication_id) + " " + unicode(self.source_type) + " " + unicode(self.molecular_state) + " " + unicode(self.constant_type)




############# This model is designed to temporarily store new data ############
######## TO display on the website, manually add to the main models ###########

### In case if there is a nesessity to delete this model ######################
### go to the file admin.py and delete there New_data #########################

class New_data(models.Model):
    new_data_id=models.AutoField(primary_key=True)
    symbol=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=200, blank=True)    
    value=models.CharField(max_length=200, blank=True)
    source_type=models.CharField(max_length=200,blank=True)
    constant_type = models.ForeignKey(Constant_type,on_delete=models.PROTECT,null=True)
    is_uncertain=models.BooleanField(default=False)    
    extra_symbol=models.CharField(max_length=200, blank=True)
    alternate_type=models.BooleanField(default=False)
    in_main_database=models.BooleanField(default=False)    
    state_in_orbyts=models.BooleanField(default=False)
    constant_in_orbyts=models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.symbol) + "_" + unicode(self.state) + "_" + unicode(self.constant_type)
