from django.conf.urls import url
from . import views



urlpatterns=[




    url(r'^molecules_list/$',views.unique_molecules, name='molecules_list'),
    url(r'^molecules_list/(?P<molecule_name>[\w\W]+)/$', views.table_for_molecule, name='molecule_details'),
    
   
    url(r'^main_table/$',views.large_table, name='large_table'),
    url(r'^molecules_list/(?P<isotopolog>[\w\W]+)/(?P<paper>[\W\W]+)/$', views.paper_info, name='paper_info'),
    url(r'^molecules_from_Huber_Herzberg_DB/$', views.molecules_from_HH, name='molecules_from_HH'),
    url(r'^molecules_from_Huber_Herzberg_DB/(?P<name>[\w\W]+)/$', views.compare_table, name="compare_table"),
]


