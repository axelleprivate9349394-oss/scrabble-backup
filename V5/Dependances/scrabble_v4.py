#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_LISENA_TIXIER_projet_V4.py : CR projet « srabble », groupe 032

LISENA <Enzo.Lisena@etu-univ-grenoble-alpes.fr>
TIXIER <Julien.Tixer@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
from Dependances.scrabble_v3 import mots_jouables

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel

# PARTIE 4 : VALEUR D'UN MOT ###################################################

def generer_dico() :
    """Dictionnaire des jetons.

    >>> jetons = generer_dico()
    >>> jetons['A'] == {'occ': 9, 'val': 1}
    True
    >>> jetons['B'] == jetons['C']
    True
    >>> jetons['?']['val'] == 0
    True
    >>> jetons['!']
    Traceback (most recent call last):
    KeyError: '!'

    Q19) Test de compréhension
    >>> jetons["K"]["occ"]
    1
    >>> jetons["Z"]["val"]
    10
    """
    jetons = {}
    with Path('lettres.txt').open(encoding='utf_8') as lettres :
        for ligne in lettres :
            l, v, o = ligne.strip().split(';')
            jetons[l] = {'occ': int(o), 'val': int(v)}
    return jetons

def init_pioche(dico):
    """
    
    - Précondition: "dico" -> dict
    - Postcondition: "pioche" -> list

    Q20) Initialise la pioche
    >>> dico = generer_dico()

    >>> init_pioche(dico)
    ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'L', 'M', 'M', 'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'U', 'U', 'V', 'V', 'W', 'X', 'Y', 'Z', '?', '?']
    
    """
    pioche = []

    for lettre in dico.keys():
        occurence = dico[lettre]["occ"]
        pioche.extend( [lettre] * occurence )

    return pioche

def valeur_mot(mot, dico):
    """
    
    - Préconditions:
        "mot" -> str ;
        "dico" -> dict ;
    - Postcondition: "valeur" -> int

    Q22) Détermine la valeur d'un "mot" en fonction des valeurs des lettres du "mot
    >>> dico = generer_dico()

    >>> valeur_mot("BEBE", dico)
    8
    >>> valeur_mot("PARADISIAQUE", dico)
    22

    """
    valeur = 0
    for lettre in mot:
        valeur += dico[lettre]["val"]
    
    return valeur

def meilleur_mot(motsfr, ll, dico):
    """
    - Préconditions:
        "dico" -> dict ;
        "motsfr" & "ll" -> list ;
    - Postcondition: "meilleur_mot" -> str

    Q23) Détermine le meilleur mot jouable
    >>> motsfr = ["COURIR", "PIED", "DEPIT", "TAPIR", "MARCHER"]
    >>> ll = ["P", "I", "D", "E", "T", "A", "R"]
    >>> dico = generer_dico()

    >>> meilleur_mot(motsfr, ll, dico)
    "DEPIT"

    """
    mots = mots_jouables(motsfr, ll)

    meilleure_valeur = 0
    meilleur_mot = ""

    for mot in mots:

        valeur = valeur_mot(mot, dico)
        if valeur > meilleure_valeur:
            meilleur_mot = mot
            meilleure_valeur = valeur

    return meilleur_mot

def meilleurs_mots(motsfr, ll, dico):
    """

    - Préconditions:
        "dico" -> dict ;
        "motsfr" & "ll" -> list ;
    - Postcondition: "meilleur_mot" -> list

    Q24) Détermine le(s) meilleur(s) mot(s) jouable(s)
    >>> motsfr = ["COURIR", "PIED", "DEPIT", "TAPIR", "MARCHER"]
    >>> motsfr_2 = ["COURIR", "PIED", "DEPIT", "TAPIR", "TIPED"]
    >>> ll = ["P", "I", "D", "E", "T", "A", "R"]
    >>> dico = generer_dico()

    >>> meilleurs_mots(motsfr, ll, dico)
    ["DEPIT"]
    >>> meilleurs_mots(motsfr_2, ll, dico)
    ["DEPIT", "TIPED"]

    """
    mots = mots_jouables(motsfr, ll)

    meilleure_valeur = valeur_mot( meilleur_mot(motsfr, ll, dico), dico )

    meilleurs_mots = []

    for mot in mots:
        if valeur_mot(mot, dico) == meilleure_valeur:
            meilleurs_mots.append(mot)
            
    return meilleurs_mots

if __name__ == "__main__":
    dico = generer_dico()

    print( dico )