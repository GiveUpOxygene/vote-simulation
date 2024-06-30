from Candidate import *
from Participant import *


#On test l'initialisation des attributs
# c : Candidat
c1=Candidate("Karim","Benzema",9,9)
print(c1)
print(c1.id)
print(c1.firstName)
print(c1.lastName)
print(c1.pos)
#On test l'égalité entre candidats
c3=c1
print(c3==c1)

c4=Candidate("Karim","Benzema",9,9)
print(c4)
print(c4==c1)


#On teste la méthode static nextId
print(Candidate.nextId())

