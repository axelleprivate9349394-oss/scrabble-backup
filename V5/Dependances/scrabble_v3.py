#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_LISENA_TIXIER_projet_V3.py : CR projet « srabble », groupe 032

LISENA <Enzo.Lisena@etu-univ-grenoble-alpes.fr>
TIXIER <Julien.Tixer@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel

# PARTIE 3 : CONSTRUCTIONS DE MOTS #############################################

def generer_dictfr(nf='littre.txt') :
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    
    with Path(nf).open(encoding='utf_8') as fich_mots :
        for line in fich_mots : mots.append(line.strip().upper())
    return mots

def select_mot_initiale(motsfr, let):
    """

    - Préconditions: 
        "motsfr" -> list ; 
        "let" -> str ;
    - Postcondition: "motsfr_let" -> list

    Q13) Renvoie tous les mots possibles du scrabble où la lettre "let" est au début du mot.

    >>> len( select_mot_initiale( generer_dictfr(), "Z") )
    229

    """

    motsfr_let = []

    for mot in motsfr:
        if mot[0].lower() == let.lower():
            motsfr_let.append(mot)

    return motsfr_let

def select_mot_longueur(motsfr, lgr):
    """

    - Préconditions: 
        "motsfr" -> list ; 
        "lgr" -> int ;
    - Postcondition: "motsfr_lgr" -> list

    Q14) Renvoie tous les mots possibles du scrabble où la longueur du mot est égale à "lgr"

    """

    motsfr_lgr = []

    for mot in motsfr:
        if len(mot) == lgr:
            motsfr_lgr.append(mot)

    return motsfr_lgr

def mot_jouable(mot, ll):
    """

    - Préconditions: 
        "mot" -> str ; 
        "ll" -> list ;
    - Postcondition: "success" -> bool

    Q15 & 16) Permet de savoir si on peut écrire le "mot" à l'aide des lettres dans "ll" (en comptant les jokers)

    >>> mot_jouable("PATATE", ["P", "T", "A", "Z", "C", "B", "?"])
    False

    >>> mot_jouable("ENJEU", ["E", "J", "N", "Z", "U", "B", "?"])
    True

    """
    temp_ll = ll.copy()

    success = True

    i = 0
    while success and i < len(mot):
        lettre = mot[i]

        lettre_apparait = lettre in temp_ll
        joker_apparait = JOKER in temp_ll

        if lettre_apparait:
            temp_ll.remove(lettre)

        elif joker_apparait:
            temp_ll.remove(JOKER)

        success = success and (lettre_apparait or joker_apparait)
        
        i += 1
    
    return success

def mots_jouables(motsfr, ll):
    """

    - Préconditions: "motsfr" & "ll" -> list ;
    - Postcondition: "liste_mots" -> list

    Q17) Renvoie la liste des mots qu'on peut faire avec les lettres de notre main ("ll")
    
    """
    liste_mots = []

    for mot in motsfr:

        if mot_jouable(mot, ll):
            liste_mots.append(mot)
    
    return liste_mots

def generer_mots_jouables(lettres_main, lettres_plateau, nb_lettres_manquantes):
    """
    - Préconditions: 
        "lettres_main" & lettres_plateau -> list ; 
        "nb_lettres_manquantes" -> int ;
    - Postcondition: "liste_mots_jouables" -> list

    Q18) Genere une liste de mots jouables avec "les lettre du plateau", "les lettres de notre main" 
    avec un certain "nombre de lettres manquantes"

    """
    mots_fr = generer_dictfr()

    lgr_min = len(lettres_main) + nb_lettres_manquantes
    lgr_max = len(lettres_main) + len(lettres_plateau) + nb_lettres_manquantes

    mot_lgr = []

    for lgr in range(lgr_min, lgr_max + 1):
        mot_lgr.extend(select_mot_longueur(mots_fr, lgr))

    main_totale = lettres_main + lettres_plateau + [JOKER] * nb_lettres_manquantes
    liste_mots_jouables = mots_jouables(mot_lgr, main_totale)

    return liste_mots_jouables

if __name__ == "__main__":
    """

    TEST) Programme principal

    """
    mots_fr = generer_dictfr()

    main = ["C", "A", "C"]
    lettres_plateau = ["A"]
    print(generer_mots_jouables(main, lettres_plateau, 0))