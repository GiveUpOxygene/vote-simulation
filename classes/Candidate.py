
from Participant import *

class Candidate(Participant) :
    """
    Classe définissant un Candidat caractérisée par :
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - un flottant vote correspondant au vote reçu / points reçu
    """
    
    def __init__ (self, firstName, lastName, x, y, vote=0) :
        """ str x str x int x int-> Candidate
        constructeur de candidat
        """
        super().__init__(firstName, lastName, x, y)
        self.label = "Candidate_n° "+str(self.id)
        self.vote=vote

    def __repr__(self) :
        """ -> str
        renvoie une description du candidat sous la forme d'une chaîne
        de caractères contenant son id, son Prénom et son Nom
        elle permet d'utiliser print pour les candidats
        """

        return self.label+" "+super().__repr__()+" [ "+str(self.pos[0])+" , "+str(self.pos[1])+" ]"

    def __eq__(self, other) :
        """ Val -> bool
        rend le booléen vrai si le candidat est égal à other, faux sinon
        elle permet que == fonctionne pour les candidats
        Attention : ne teste que type et identifiant !
        """
        return type(self) == type(other) and self.id == other.id
    
    def voted(self,n=1):
        """->None
        On ajoute n à l'attribut vote"""
        self.vote+=n
    
    def resetVote(self):
        """->None
        l'attribue vote est réinitialisé à 0"""
        self.vote=0






