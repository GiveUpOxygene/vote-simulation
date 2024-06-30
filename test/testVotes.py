from votes import *

XMAX=100
YMAX=100

def randomParticipant(is_candidate,x=None,y=None):
    if x==None or y==None:
        x=np.random.randint(0, XMAX)
        y=np.random.randint(0, YMAX)
        firstname=firstNameGenerator()
        lastname=lastNameGenerator()
        if is_candidate==True:
            return Candidate(firstname,lastname,x,y)
        else:
            return Voter(firstname,lastname,x,y)
    
###Tests
if __name__ == '__main__':
    np.random.seed(42)
    dictCandidates=dict()
    dictVoters=dict()
    for a in range (0,5):
        c=randomParticipant(True)
        dictCandidates[c.id]=c
    for a in range (0,50):
        v=randomParticipant(False)
        dictVoters[v.id]=v

    borda(dictCandidates,dictVoters)
    resetElections(dictCandidates,dictVoters)
    plurality(dictCandidates,dictVoters)
    resetElections(dictCandidates,dictVoters)
    copeland(dictCandidates,dictVoters)
    resetElections(dictCandidates,dictVoters)
    simpson(dictCandidates,dictVoters)



    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    area=QWidget()
    area.setGeometry(250,150,650,510)
    t=ParticipantTable(area,dictCandidates,dictVoters)
    t.move(0,0)
    area.show()
    app.exec_()




