import sys
import os
from PyQt5.QtCore import Qt,pyqtSignal,QRect
from PyQt5.QtWidgets import QMainWindow,QApplication,QMenu,QAction,QWidget,QPushButton,QHBoxLayout,QLineEdit,QDialog,QMessageBox,QLabel,QSplitter,QColorDialog,QTabWidget,QCheckBox
from PyQt5.QtGui import QPixmap,QPainter,QPen,QColor,QIcon,QPalette    
from collections import OrderedDict
import numpy as np
from Classes import *

def firstNameGenerator():
    """->str
    retourne un prénom aléatoire du fichier prenoms.txt contenant 2666 prénoms"""
    name="doc/prenoms.txt"
    file=open(name,"r")
    linenumber=2666
    for i in range(0,np.random.randint(1, 2666)):
        line=file.readline()
        words=line.split("\n")
    return words[0]

def lastNameGenerator():
    """->str
    retourne un nom aléatoire du fichier noms.txt"""
    name="doc/noms.txt"
    file=open(name,"r")
    linenumber=2666
    for i in range(0,np.random.randint(1, 6338)):
        line=file.readline()
        words=line.split("\n")
    return words[0]

def rating(candidates, n=-1):
    """Dict[int,Candidate] x Optional[int] -> Dict[int,Candidate]
    Classe les candidats par ordre décroissant des votes reçus"""
    score= { k : v.vote for (k,v) in candidates.items() }
    sortedscore=(sorted(score.items(), key=lambda t: t[1]))
    sortedscore2=list(reversed(sortedscore))
    c=candidates
    results= [(k[0],c[k[0]]) for k in sortedscore2]
    return OrderedDict(results)
            
def resetElections(candidates, voters):
    """Dict[Candidate] x Dict[Voter] -> None
    Réinitialise les votes reçus à 0 et les attributs hasVoted à False"""
    for (k,c) in candidates.items():
        c.resetVote()
    for (k,v) in voters.items():
        v.resethasVoted()

def distance(p1, p2):
    """Participant x Partcipant -> float
    Renvoie la distance entre deux Participants
    """
    return np.linalg.norm(np.array([p1.pos[0], p1.pos[1]]) - np.array([p2.pos[0], p2.pos[1]]))

def n_best_votes(candidates, voters, n=-1):
    """Dict[int,Candidate] x Dict[int,Voter] x Optional[int] -> Dict[int,List[int]]
    (Renvoie les n meilleurs candidats pour chaque votant
    Args:
        candidates (dict): dictionnaire de la forme : id_candidate : Candidate
        voters (dict): dictionnaire de la forme : id_voter : Voter
        n (int, optional): nombre de candidats à renvoyer. Defaults to -1, renvoie tous les candidats."""

    if n == -1:
        n = len(candidates)
    dico = dict()
    for (k1,v1) in voters.items():
        dico[k1] = {}
        # Calcul de la distance entre le votant et chaque candidat
        for (k2,v2) in candidates.items():
            dico[k1][k2] = distance(v1,v2)
    # Tri des candidats par distance
    #dictResults : Dict[int,Dict[int,float]]
    dictResults = {voter: {candidate: dico[voter][candidate] for candidate in sorted(dico[voter], key=dico[voter].get)[:n]} for voter in dico}
    #results : Dict [int,List[int]]
    results = { idvoter : [k for k in v] for (idvoter,v) in dictResults.items() }
    return results

def borda(candidates, voters, n=-1):
    """Dict[int,Candidate] x Dict[int,Voter] x Optional[int]-> None
    effectue un vote de Borda 
    Args:
        candidates (dict): dictionnaire de la forme : id_candidate : Candidate
        voters (dict): dictionnaire de la forme : id_voter : Voter
        n (int, optional): nombre de candidats à renvoyer. Defaults to -1, renvoie tous les candidats.
    """
    best = n_best_votes(candidates, voters, n)
    for (voter,listCandidates) in best.items():
        if not(voters[voter].hasVoted):
            for k in range(len(listCandidates)):
                (voters[voter]).voteFor(candidates[listCandidates[k]],(len(listCandidates)-1-k))

def plurality(candidates, voters):
    """Dict[int,Candidate] x Dict[int,Voter]-> None
    Args:
        candidates (dict): dictionnaire de la forme : id_candidate : Candidate
        voters (dict): dictionnaire de la forme : id_voter : Voter
        n (int, optional): nombre de candidats à renvoyer. Defaults to -1, renvoie tous les candidats.
    """
    best = n_best_votes(candidates, voters, 1)
    for (voter,listCandidates) in best.items():
        if not(voters[voter].hasVoted):
            (voters[voter]).voteFor(candidates[listCandidates[0]])

def veto(candidates, voters):
    """Dict[Candidate] x Dict[Voters]-> None
    effectue un vote de Veto et renvoie le résultat
    Chaque dernière place rapporte un point négatif

    Args:
        candidates (dict): dictionnaire de la forme : id_candidate : Candidate
        voters (dict): dictionnaire de la forme : id_voter : Voter
    """
    best = n_best_votes(candidates, voters)
    for (voter,listCandidates) in best.items():
        if not(voters[voter].hasVoted):
            (voters[voter]).voteFor(candidates[listCandidates[len(listCandidates)-1]],-1)

def approval(candidates, voters, n=1):
    """Dict[Candidate] x Dict[Voters] x Optional[int]-> None
    effectue un vote d'approbation et renvoie le résultat
    Chaque candidat au dessus de la nième place gagne un point positif
    /!\ n doit être inférieur au nombre de candidats
    /!\ n est par défaut à 1 <=> pluralité 

    Args:
        candidates (dict): dictionnaire de la forme : id_candidate : Candidate
        voters (dict): dictionnaire de la forme : id_voter : Voter
    """
    best = n_best_votes(candidates, voters, n)
    for (voter,listCandidates) in best.items():
        if not(voters[voter].hasVoted):
            for c in listCandidates:
                (voters[voter]).voteFor(candidates[c])

def stv(candidates:dict,voters:dict):
    """Dict[int,Candidate] x Dict[int,Voter] -> Optional[Dict[int,int],int]
    Règles par éliminations successives, (fonction récursive)
    Args:
        candidates (dict): candidats (déf dans main)
        voters (dict): votants (déf dans main)
    Returns:
        int: l'id du vainqueur
    """
    score = {candidate:0 for candidate in candidates}
    best=n_best_votes(candidates, voters)
    for (candidate,v) in best.items():
        score[v[0]]+=1
    for (candidate,v) in score.items():
        if v>(len(candidate)/2):
            return candidates[candidate]
        else:
            #Enlever du dictionnaire candidates le candidat avec le moins de première place 
            return stv(candidates,voters)

#----------------- Méthodes de Condorcet -----------------#

def condorcet_duel(candidates:dict, voters:dict, id1:int, id2:int, score:bool=False):
    """Dict[Candidate] x Dict[Voters] x int x int x Optional[bool] ->Optional[Dict[int,int],int]
    Duel de Condorcet entre deux candidats

    Args:
        voters (dict): Voter (déf dans main)
        candidats (dict): Candidate
        id1 (int): id du candidat 1
        id2 (int): id du candidat 2

    Returns:
        int: l'id du vainqueur, -1 si égalité
    """
    score_id1 = 0
    score_id2 = 0
    dictCandidates={id1:candidates[id1],id2:candidates[id2]}
    best = n_best_votes(dictCandidates,voters)
    for (k,v) in best.items():
        if v[0]==id1:
            score_id1+=1
        else:
            score_id2+=1
    if score:
        return {id1:score_id1, id2:score_id2}
    else:
        return id1 if score_id1 > score_id2 else -1 if score_id2 == score_id1 else id2


    
def copeland(candidates:dict, voters:dict, withScore=False):
    """Dict[int,Candidate] x Dict[int,Voter] x Optional[bool]-> Optional[Dict[int,int],int]
    Méthode de Copeland
    Args:
        candidates (dict): candidats (déf dans main)
        voters (dict): votants (déf dans main)
    Returns:
        int: l'id du vainqueur
    """
    score = {candidate:0 for candidate in candidates}
    for id1 in candidates:
        for id2 in candidates:
            if id1 != id2:
                res = condorcet_duel(candidates, voters, id1, id2)
                score[id1] += 1 if res == id1 else 0 if res == id2 else 0.5
    id_vainqueur = 1
    for id in range(1,len(score)):
        if score[id] > score[id_vainqueur]:
            id_vainqueur = id
    if withScore:
        return score
    return id_vainqueur

def simpson(candidates:dict,voters:dict,withScore=False):
    """Dict[int,Candidate] x Dict[int,Voter] x Optional[bool]-> Optional[Dict[int,int],int]
    Méthode de Simpson
    Args:
        candidates (dict): candidats (déf dans main)
        voters (dict): votants (déf dans main)
    Returns:
        int: l'id du vainqueur
    """
    score = {candidate:(len(voters)) for candidate in candidates}
    for id1 in candidates:
        for id2 in candidates:
            if id1 != id2:
                res = condorcet_duel(candidates, voters, id1, id2, True)
                affiche_dico(res)
                score[id1] = min(score[id1], res[id1])    
    id_vainqueur = 1
    for id in range(1,len(score)):
        if score[id] > score[id_vainqueur]:
            id_vainqueur = id
    if withScore:
        return score
    return id_vainqueur



#----------------- Méthodes à plusieurs tours -----------------#



#----------------- Fonctions de débug -----------------#

def affiche_dico(dico):
    """Dict[Participant]->NoneType
    Affiche un dictionnaire de la forme : id_participant: Participant
    Fonction de débug
    Args:
        dico (dict): dictionnaire à afficher
    """
    for (k,v) in dico.items():
        print(k, v)
