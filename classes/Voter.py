from Participant import *

class Voter(Participant) :
    """
    Classe définissant Votant caractérisée par :
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - un booléen hasVoted égale à True si le votant a voté, False sinon
    """

    def __init__ (self, firstName, lastName, x, y, hasVoted=False) :
        """ str x str x int x int-> Votant
        constructeur de votant
        """
        super().__init__(firstName, lastName, x, y)
        self.label="Votant_n° "+str(self.id)
        self.hasVoted=hasVoted
        
    def __repr__(self) :
        """ -> str
        renvoie une description du votant sous la forme d'une chaîne
        de caractères contenant son id, son Prénom,son Nom et sa position
        elle permet d'utiliser print pour les votants
        """

        return self.label+" "+super().__repr__()+" [ "+str(self.pos[0])+" , "+str(self.pos[1])+" ]"
    
    def __eq__(self, other) :
        """ Val -> bool
        rend le booléen vrai si le votant est égal à other, faux sinon
        elle permet que == fonctionne pour les votants
        Attention : ne teste que type et identifiant !
        """
        return type(self) == type(other) and self.id == other.id
    
    def voteFor(self,candidate,n=1):
        """Candidate->None
        le candidat reçoit n vote et l'attribut hasVoted prend la valeur True"""
        candidate.voted(n)
        self.toVote()

    def toVote(self):
        """->None
        Le booléen hasVoted prend la valeur True"""
        self.hasVoted=True

    def resethasVoted(self):
        """->None
        Le booléen hasVoted prend la valeur False """
        self.hasVoted=False


