#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_LISENA_TIXIER_projet_V6.py : CR projet « srabble », groupe 032

LISENA <Enzo.Lisena@etu-univ-grenoble-alpes.fr>
TIXIER <Julien.Tixer@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 4  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel

# PARTIE 6 : PLACEMENT DE MOT ###################################################

def lire_coords():
    """

    - Précondition: //
    - Postcondition: 
        * coords -> tuple ;

    Q29) Demande au joueur des coordonnées, les filtre jusqu'à correspondre à une case vide du plateau
    
    """

    x = int( input("- Coordonnée x: ") )
    y = int( input("- Coordonnée y: ") )

    while (x < 0 or x >= TAILLE_PLATEAU) or (y < 0 or y >= TAILLE_PLATEAU):
        x = int( input("- Coordonnée x: ") )
        y = int( input("- Coordonnée y: ") )
    
    return x, y

def tester_placement(plateau, i, j, dir, mot):
    """
    
    - Préconditions:
        * "plateau" -> list ;
        * "i" & "j" -> int ;
        * "dir" & "mot" -> str ;
    - Postcondition: 
        * "liste_lettres" -> list ;

    Q30) Détermine la liste des lettres nécessaires pour placer ce mot à cet endroit dans ce sens (si possible).
    On s'assurera de juste vérifier si on peut placer le mot (et pas des contraintes du scrabble sur le placement
    des mots)
    ** Ici, on vérifie les conditions suivantes: **
        - Longueur du "mot" par rapport à la position de départ et la taille du plateau
        - Si d'autres lettres gênent au placement du mot
    ** On cherchera dans la fonction suivante à: **
        - Vérifier que le mot est bien formé grace à une autre lettre (sauf si c'est le premier mot placé de la partie)
        - Vérifier que le mot complete d'autres mots correctement s'il est en collision avec d'autres lettres
        * EXEMPLE: si on cherche à placer "LAC" en (x, y) = (2, 1) *
        [" ", " ", " ", " "]
        [" ", " ", " ", " "]
        [" ", "L", "I", "T"] 
        [" ", " ", " ", " "]

        [" ", " ", " ", " "]
        [" ", "L", "A", "C"]
        [" ", "L", "I", "T"]
        [" ", " ", " ", " "]
        On forme aussi trois autres mots, "LL", "AI", "CT" qui ne sont pas compatibles !

    >>> TAILLE_PLATEAU = 4
    >>> plt_1 = [
    >>> [" ", " ", " ", " "],
    >>> [" ", " ", "L", " "],
    >>> [" ", " ", "Z", " "],
    >>> [" ", " ", " ", " "] ]

    >>> plt_2 = [
    >>> [" ", " ", " ", " "],
    >>> [" ", "L", " ", " "],
    >>> [" ", " ", "A", " "],
    >>> [" ", " ", " ", " "] ]

    >>> plt_3 = [
    >>> [" ", " ", " ", " "],
    >>> [" ", " ", " ", "L"],
    >>> [" ", " ", " ", " "],
    >>> [" ", " ", " ", " "] ]

    >>> tester_placement(plt_1, 2, 1, "vertical", "LAC")
    []

    >>> tester_placement(plt_2, 2, 1, "vertical", "LAC")
    ["L", "C"]
    >>> tester_placement(plt_2, 1, 1, "horizontal", "LAC")
    ["A", "C"]

    >>> tester_placement(plt_3, 3, 1, "horizontal", "LAC")
    []
    >>> tester_placement(plt_3, 2, 1, "vertical", "LAC")
    ["L", "A", "C"]
    
    """
    liste_lettres = []
    temp_liste_lettre = []

    horizontal = dir == "horizontal"
    vertical = dir == "vertical"

    if horizontal:
                
        ### CECI EST "FONCTIONNEL" MAIS SCRABBLE DE MERDE DE FDP C PAS LES BONNES REGLES, jle laisse en template
        # Faire petit dessin pour comprendre
        # parcourt_gauche = (i + 1) - len(mot) >= 0

        # if parcourt_gauche:
        #     placable_gauche = True
        #     liste_lettres_gauche = []

        #     temp_i = 0
        #     # Parcourt à gauche en horizontal
        #     for x in range(i, -1, -1):
        #         lettre_mot = mot[temp_i]
        #         lettre_plateau = ligne[x]

        #         if lettre_plateau == " ":
        #             liste_lettres_gauche.append(mot[temp_i])
        #         else:
        #             placable_gauche = placable_gauche and lettre_mot == lettre_plateau

        #         temp_i += 1

        #     if placable_gauche:
        #         liste_lettres += liste_lettres_gauche

        # Faire petit dessin pour comprendre
        parcourt_droite = TAILLE_PLATEAU - i - len(mot) >= 0
        ligne = plateau[j]

        # if not placable_gauche and parcourt_droite:
        if parcourt_droite:
            placable_droite = True

            temp_i = 0

            # Parcourt à droite en horizontal
            for x in range( len(mot) ):
                indice_plateau = x + i
                lettre_plateau = ligne[indice_plateau]

                lettre_mot = mot[temp_i]

                if lettre_plateau == " ":
                    temp_liste_lettre.append( lettre_mot )
                else:
                    placable_droite = placable_droite and lettre_mot == lettre_plateau

                temp_i += 1

            if placable_droite:
                liste_lettres += temp_liste_lettre

    elif vertical:
        # Faire petit dessin pour comprendre
        parcourt_bas = TAILLE_PLATEAU - j - len(mot) >= 0
        
        # On est obligé de la construire
        colonne = []
        for y in range(TAILLE_PLATEAU):
            colonne.append( plateau[y][i] )

        if parcourt_bas:
            placable_bas = True

            temp_j = 0

            # Parcourt en bas en vertical
            for y in range( len(mot) ):
                indice_plateau = y + j
                lettre_plateau = colonne[indice_plateau]

                lettre_mot = mot[temp_j]

                if lettre_plateau == " ":
                    temp_liste_lettre.append(mot[temp_j])
                else:
                    placable_bas = placable_bas and lettre_mot == lettre_plateau

                temp_j += 1

        if placable_bas:
            liste_lettres += temp_liste_lettre
    

    return liste_lettres

def placer_mot(plateau, lm, mot, i, j, dir):
    """

    - Préconditions:
        * "plateau" & "lm" -> list ;
        * "i" & "j" -> int ;
        * "dir" & "mot" -> str ;

    - Postcondition:
        * "sucess" -> bool ;
    Q31) Placer le "mot" sur le "plateau" en s'assurant de bien pouvoir
    placer le mot. On utilisera la fonction du dessus et:
    ** On cherchera à: **
    - Vérifier que le mot est bien formé grace à une autre lettre (sauf si c'est le premier mot placé de la partie)
    - Vérifier que le mot complete d'autres mots correctement s'il est en collision avec d'autres lettres
    * EXEMPLE: si on cherche à placer "LAC" en (x, y) = (2, 1) *
    [" ", " ", " ", " "]
    [" ", " ", " ", " "]
    [" ", "L", "I", "T"] 
    [" ", " ", " ", " "]

    [" ", " ", " ", " "]
    [" ", "L", "A", "C"]
    [" ", "L", "I", "T"]
    [" ", " ", " ", " "]
    On forme aussi trois autres mots, "LL", "AI", "CT" qui ne sont pas compatibles !

    """

    # FONCTION

def valeur_mot_v2(plateau, positions_depart, direction, mot, dico):
    """
    
    - Préconditions:
        * "plateau" -> list ;
        * "positions_depart" -> tuple ;
        * "direction" & "mot" -> str ;
        * "dico" -> dict ;
    - Postcondition:
        * "valeur" -> int ;

    Q32) Détermine la valeur d'un "mot" en fonction des valeurs des lettres du "mot" ainsi que sa
    position sur le plateau

    """

    # On cherchera à parcourir le plateau de la position de départ et de sa direction, on mettra la case
    # bonus dans une liste (parcours du mot de gauche à droite) : on s'assurera d'avoir placé le mot AVANT d'appliquer la valeur du mot
    # On pourra meme éviter ("positions_depart", "direction") et directement mettre "valeur_bonus" en parametre dans la fonction !

    # Exemple: on a placé "VALEUR" à l'horizontal on aura
    # valeur_bonus = ["MT", "", "", "LD", "", ""] et on appliquera le bonus à l'aide d'un dico (ici "MT" = "*" etc... voir v1)
    """
    Code extrait de V1
        bonus_to_symbole = {
        '': '',
        "MT": "*",
        "MD": "+",
        "LT": "/",
        "LD": "-"
    }
    """
    
    valeur = 0
    for lettre in mot:
        valeur += dico[lettre]["val"]
    
    return valeur

if __name__ == "__main__":
    """
    TESTS
    """
    plt_1 = [
    [" ", " ", " ", " "],
    [" ", " ", "L", " "],
    [" ", " ", "Z", " "],
    [" ", " ", " ", " "] ]

    plt_2 = [
    [" ", " ", " ", " "],
    [" ", "L", " ", " "],
    [" ", " ", "A", " "],
    [" ", " ", " ", " "] ]

    plt_3 = [
    [" ", " ", " ", " "],
    [" ", " ", " ", "L"],
    [" ", " ", " ", " "],
    [" ", " ", " ", " "] ]

    print( tester_placement(plt_1, 2, 1, "vertical", "LAC") )

    print( tester_placement(plt_2, 2, 1, "vertical", "LAC") )
    print( tester_placement(plt_2, 1, 1, "horizontal", "LAC") )

    print( tester_placement(plt_3, 3, 1, "horizontal", "LAC") )
    print( tester_placement(plt_3, 2, 1, "vertical", "LAC") )