
class Participant :
    """
    Classe définissant un Participant caractérisée par :
        - un identifiant
        - une chaîne de caractère correspondant au Prénom
        - une chaîne de caractère correspondant au Nom
        - une liste pos de coordonnées [x,y] correspondant à la positions du Participant
    """
    idCounter=0
    def __init__ (self,firstName, lastName, x, y) :
        """ str x str x int x int x bool-> Participant
        constructeur de participant
        """
        Participant.idCounter+=1
        self.id=Participant.idCounter
        self.firstName = firstName
        self.lastName = lastName
        self.pos=[int(x),int(y)]

    def __repr__(self) :
        """ -> str
        renvoie une description du Participant sous la forme d'une chaîne
        de caractères contenant son Prénom et son Nom
        elle permet d'utiliser print pour les participants
        """

        return self.firstName+" "+self.lastName


    def __eq__(self, other) :
        """ Val -> bool
        rend le booléen vrai si le participant est égal à other, faux sinon
        elle permet que == fonctionne pour les participants
        Attention : ne teste que type et identifiant !
        """
        return type(self) == type(other) and self.id == other.id
    
    def move(self,x,y):
        """int x int ->None
        déplace le participant aux coordonnées [x,y]"""
        self.pos[0]=x
        self.pos[1]=y

    @staticmethod

    def nextId():
        """->str
        renvoie l'id du prochain participant créé"""
        return str(Participant.idCounter+1)





