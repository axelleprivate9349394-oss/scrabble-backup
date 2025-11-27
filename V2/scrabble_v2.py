#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_LISENA_TIXIER_projet_V2.py : CR projet « srabble », groupe 032

LISENA <Enzo.Lisena@etu-univ-grenoble-alpes.fr>
TIXIER <Julien.Tixer@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

import random

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel


# PARTIE 2 : LA PIOCHE ########################################################

def init_pioche_alea():
    """

    - Précondition: //
    - Postcondition: 
        * "liste_alea_jetons" -> list ;

    Q7) Générer une liste aléatoire de jetons: où (A, Z) forcément une fois + 74 autres caracs majs + 2 jokers
    
    """
    liste_alea_jetons = [JOKER] * 2

    for i in range(26):
        liste_alea_jetons.append( chr( ord("A") + i ) )

    for j in range(74):
        lettre_aleatoire = chr(random.randint(ord("A"), ord("Z")))
        liste_alea_jetons.append( lettre_aleatoire )

    # Si on souhaite randomiser 2 fois. (avec les indices = positions)
    random.shuffle(liste_alea_jetons)

    return liste_alea_jetons

def piocher(x, sac):
    """
    - Préconditions: 
        * "x" -> int ; 
        * "sac" -> list ;
    - Postcondition: 
        * "pioche" -> list ;

    Q8) Pioche au hasard "x" jetons dans le "sac"
    """
    pioche = []

    for i in range(x):
        index_rand = random.randint(0, len(sac)-1)
        jeton = sac[index_rand]

        pioche.append(jeton)

        sac.remove(jeton)
    
    return pioche

def completer_main(main, sac):
    """

    - Préconditions: 
        * "main" & "sac" -> list ;
    - Postcondition: //

    Q9) Complète la "main" du joueur pour qu'il aie 7 jetons (si possible)

    """

    while len(main) < 7 and len(sac) > 0:
        main += piocher(1, sac)

def echanger(jetons, main, sac):
    """

    - Préconditions: 
        * "jetons" & "main" & "sac" -> list ; 
    - Postcondition: 
        * "success" -> bool ;

    Q10) Effectue un échange entre les jetons de la "main" du joueur et ceux qu'il propose
    d'échanger ("jetons") contre ceux du "sac" (si possible)

    """
    success = len(sac) >= 7

    temp_sac = []

    i = 0
    while success and i < len(jetons):
        jeton = jetons[i]
        success = success and jeton in main

        if success:
            main.remove(jeton)
            temp_sac.append(jeton)
        
        i += 1
    
    if success:
        main += piocher(len(jetons), sac)
        sac += temp_sac
    else:
        main += temp_sac

    return success

if __name__ == "__main__":
    """

    Q11) Programme Principal permettant de tester nos fonctions

    """
    # On réduit volontairement la taille de la liste pour une meilleure compréhension
    sac = init_pioche_alea()[:17]

    main_p1 = piocher(7, sac)
    main_p2 = piocher(7, sac)

    jouer = True

    p = "P1"
    T = {
        "P1": main_p1,
        "P2": main_p2
    }

    while jouer:
        main_p = T[p]

        jetons_changer = []
        print(f"- SAC: {sac}")
        print(f"- Tour de {p}", main_p)

        jeton_changer = input(f"[{p}] Quelles jetons veux tu échanger? ")
        while jeton_changer != "stop":
            jetons_changer.append(jeton_changer)

            jeton_changer = input(f"[{p}] Quelles jetons veux tu échanger? ")
        
        success = echanger(jetons_changer, main_p, sac)
        print(f"[{p}] CHANGE JETONS {success}")
        print()

        if p == "P1":
            p = "P2"
        else:
            p = "P1"