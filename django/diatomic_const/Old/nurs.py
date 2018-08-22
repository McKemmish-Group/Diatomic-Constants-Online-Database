from data_management.models import *




molecule_type='LiO'

data=Diatomic_constant.objects.all()



titles_test=[]
papers=[]

for i in data:

    if (i.molecular_state.symbol==molecule_type
        and i.reference_publication.title not in titles_test):
        titles_test.append(i.reference_publication.title)
        papers.append(i)


print(titles_test)
