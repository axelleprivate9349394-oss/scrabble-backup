#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_LISENA_TIXIER_projet_V1.py : CR projet « srabble », groupe 032

LISENA <Enzo.Lisena@etu-univ-grenoble-alpes.fr>
TIXIER <Julien.Tixer@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

import pygame
from pygame.locals import *

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel


# PARTIE 1 : LE PLATEAU ########################################################

def symetrise_liste(lst) :
    """
    Auxilliaire pour Q1 : symétrise en place la liste lst.
    EB : modification de lst.

    >>> essai = [1,2] ; symetrise_liste(essai) ; essai
    [1, 2, 1]
    >>> essai = [1,2,3] ; symetrise_liste(essai) ; essai
    [1, 2, 3, 2, 1]
    """
    copie_lst = list(lst)
    for i in range(2, len(copie_lst)+1) : lst.append(copie_lst[-i])


def init_bonus() :
    """

    - Précondition: //
    - Postcondition: 
        * "plt_bonus" -> list ;

    Q1) Initialise le plateau des bonus

    """
    # Compte-tenu  de  la  double   symétrie  axiale  du  plateau,  on
    # a  7  demi-lignes  dans  le  quart  supérieur  gauche,  puis  la
    # (demi-)ligne centrale,  et finalement  le centre. Tout  le reste
    # s'en déduit par symétrie.
    plt_bonus = [  # quart-supérieur gauche + ligne et colonne centrales
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MT'],
        [''  , 'MD', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'MD', ''  , ''  , ''  , 'LD', ''],
        ['LD', ''  , ''  , 'MD', ''  , ''  , ''  , 'LD'],
        [''  , ''  , ''  , ''  , 'MD', ''  , ''  , ''],
        [''  , 'LT', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'LD', ''  , ''  , ''  , 'LD', ''],
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MD']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plt_bonus : symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plt_bonus)

    return plt_bonus

def init_jetons() :
    """

    - Précondition: //
    - Postcondition: 
        * "plt_jetons" -> list ;

    Q2) Initialise le plateau des jetons
    """

    plt_jetons = [ [" " for x in range(TAILLE_PLATEAU)] for y in range(TAILLE_PLATEAU) ]

    return plt_jetons

def dizaine(n):
    """

    - Précondition: 
        * "n" -> int ;
    - Postcondition: 
        * "position" -> str ;

    Q3.bis) Détecte une dizaine et adapte la plt_longueur du nombre

    """
    position = f"0{n}"
    if n >= 10:
        position = str(n)
    
    return position

def affiche_jetons_q3(j) :
    """

    - Précondition: 
        * "j" -> list ;
    - Postcondition: //

    Q3) Affichage des jetons sur le plateau de coordonnées (x, y)

    """
    # Plateau
    plt_jetons = j.copy()

    # TESTS AFFICHAGE
    # plt_jetons[0][0] = "A"
    # plt_jetons[4][2] = "C"

    # Espaces
    espace_x = "-" * 3
    espace_y = "|"

    # Marges (x, y)
    marge_gauche = " " * ( max(3, TAILLE_MARGE) )

    marge_num_x_debut = " " * ( max(0, TAILLE_MARGE - 3) )
    marge_num_x_fin = " "

    marge_num_y_debut = marge_gauche + " "
    marge_num_y = " " * 2

    # Affichage
    affichage_ligne = marge_gauche + (espace_y + espace_x) * TAILLE_PLATEAU + espace_y

    # Début de l'affichage
    y = 0
    colonnes_init = False
    while y < TAILLE_PLATEAU:

        # "    01  02  03 ..." : Initialisaiton des positions au dessus des colonnes.
        if not colonnes_init:
            print( marge_num_y_debut, end = "" )
            for i in range(1, TAILLE_PLATEAU + 1):
                position = dizaine(i)

                print( position, end = marge_num_y )   
            print()
            
            colonnes_init = True

        # "   |---|---|---|---|---|" : Début de ligne
        print( affichage_ligne )
        
        x = 0        
        ligne_init = False
        while x < TAILLE_PLATEAU:

            # "0X " ou "XX " : Initialisaiton des positions à gauche des lignes.
            if not ligne_init:
                position = dizaine(y + 1)
                print( marge_num_x_debut + position, end = marge_num_x_fin )

                ligne_init = True

            lettre = plt_jetons[y][x]
            case = " " + lettre + " "

            affichage_case = espace_y + case
            # "| A*" ou "|   " ou "| A "
            print( affichage_case, end = "" )

            x += 1

        # "|\n" : Fin de ligne complétée
        print( espace_y )

        y += 1

    # "   |---|---|---|---|---|" : Fin du plateau
    print( affichage_ligne )

def affiche_jetons_q4(j) :
    """

    - Précondition: 
        * "j" -> list ;
    - Postcondition: //

    Q4) Affichage des jetons et bonus sur le plateau de coordonnées (x, y)

    """
    # Plateau
    plt_jetons = j.copy()
    plt_bonus = init_bonus()

    # TESTS AFFICHAGE
    # plt_jetons[0][0] = "A"
    # plt_jetons[4][2] = "C"

    bonus_to_symbole = {
        '': '',
        "MT": "*",
        "MD": "+",
        "LT": "/",
        "LD": "-"
    }

    # Espaces
    espace_x = "-" * 3
    espace_y = "|"

    # Marges (x, y)
    marge_gauche = " " * ( max(3, TAILLE_MARGE) )

    marge_num_x_debut = " " * ( max(0, TAILLE_MARGE - 3) )
    marge_num_x_fin = " "

    marge_num_y_debut = marge_gauche + " "
    marge_num_y = " " * 2

    # Affichage
    affichage_ligne = marge_gauche + (espace_y + espace_x) * TAILLE_PLATEAU + espace_y

    # Début de l'affichage
    y = 0
    colonnes_init = False
    while y < TAILLE_PLATEAU:

        # "    01  02  03 ..." : Initialisaiton des positions au dessus des colonnes.
        if not colonnes_init:
            print( marge_num_y_debut, end = "" )
            for i in range(1, TAILLE_PLATEAU + 1):
                position = dizaine(i)

                print( position, end = marge_num_y )   
            print()
            
            colonnes_init = True

        # "   |---|---|---|---|---|" : Début de ligne
        print( affichage_ligne )
        
        x = 0        
        ligne_init = False
        while x < TAILLE_PLATEAU:

            # "0X " ou "XX " : Initialisaiton des positions à gauche des lignes.
            if not ligne_init:
                position = dizaine(y + 1)
                print( marge_num_x_debut + position, end = marge_num_x_fin )

                ligne_init = True

            lettre = plt_jetons[y][x]
            bonus = plt_bonus[y][x]
            
            case = " " + lettre
            if lettre != " " and bonus != "":
                case += bonus_to_symbole[bonus]
            else:
                case += " "

            affichage_case = espace_y + case
            # "| A*" ou "|   " ou "| A "
            print( affichage_case, end = "" )

            x += 1

        # "|\n" : Fin de ligne complétée
        print( espace_y )

        y += 1

    # "   |---|---|---|---|---|" : Fin du plateau
    print( affichage_ligne )

def draw_case(screen, taille_case, taille_font, x, y, color, lettre):
    """
    - Préconditions:
        * "screen" -> Screen ; 
        * "taille_case" & "taille_font" & "x" & "y" -> float ; 
        * "color" -> tuple (Vec3D) ; "lettre" -> str ;

    - Postcondition: //

    Q6.bis) Dessine la case sur le "screen" PyGame.

    Doc:
    # https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
    # https://www.geeksforgeeks.org/python/pygame-drawing-objects-and-shapes/
    """
    pygame.font.init()
    
    font = pygame.font.SysFont("Arial Black", taille_font)

    pygame.draw.rect(screen, color, 
                 [x, y, taille_case, taille_case], 0)
    
    text_surface = font.render(lettre, True, (0, 0, 0))

    nombre_pixels_x = text_surface.get_size()[0]
    nombre_pixels_y = text_surface.get_size()[1]

    # En théorie, c'est censé être "centré" mais ca l'est pas vraiment à +- (5 à 8) pixels :(
    texte_x = x + ( taille_case - nombre_pixels_x ) / 2
    texte_y = y + ( taille_case - nombre_pixels_y ) / 2
    screen.blit( text_surface, (texte_x, texte_y) )

    pygame.display.update()
    pygame.font.quit()

import time
def affiche_jetons_q6(j) :
    """
    
    - Précondition: 
        * "j" -> list ;
    - Postcondition: //

    Q6 BONUS) Affichage des jetons et bonus sur le plateau de coordonnées (x, y)

    """
    # Init PyGame
    pygame_x0 = 0
    pygame_y0 = 0
    pygame_delta = 3
    pygame_taille_case = 50
    pygame_taille_font = 50

    pygame.init()

    screen_x = pygame_x0 + TAILLE_PLATEAU * (pygame_taille_case + pygame_delta) + (2 * pygame_taille_case)
    screen_y = pygame_y0 + TAILLE_PLATEAU * (pygame_taille_case + pygame_delta) + (2 * pygame_taille_case)
    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption("Scrabble")

    screen.fill((255, 255, 255))
    pygame.display.update()

    # Plateau
    plt_jetons = j.copy()
    plt_bonus = init_bonus()

    # TESTS AFFICHAGE
    plt_jetons[0][0] = "A"
    plt_jetons[1][1] = "C"

    bonus_to_symbole = {
        '': '',
        "MT": "*",
        "MD": "+",
        "LT": "/",
        "LD": "-"
    }

    case_color = {
        '': (5, 107, 38),
        "MT": (255, 0, 0),
        "MD": (225, 183, 101),
        "LT": (13, 125, 175),
        "LD": (149, 196, 227)
    }

    # Espaces
    espace_x = "-" * 3
    espace_y = "|"

    # Marges (x, y)
    marge_gauche = " " * ( max(3, TAILLE_MARGE) )

    marge_num_x_debut = " " * ( max(0, TAILLE_MARGE - 3) )
    marge_num_x_fin = " "

    marge_num_y_debut = marge_gauche + " "
    marge_num_y = " " * 2

    # Affichage
    affichage_ligne = marge_gauche + (espace_y + espace_x) * TAILLE_PLATEAU + espace_y

    # Début de l'affichage
    colonnes_init = False
    for y in range(TAILLE_PLATEAU):
        pygame_y = pygame_y0 + pygame_taille_case * (y + 1) + pygame_delta * (y + 1)

        # "    01  02  03 ..." : Initialisaiton des positions au dessus des colonnes.
        if not colonnes_init:
            print( marge_num_y_debut, end = "" )
            for i in range(1, TAILLE_PLATEAU + 1):
                position = dizaine(i)

                print( position, end = marge_num_y )   
            print()
            
            colonnes_init = True

        # "   |---|---|---|---|---|" : Début de ligne
        print( affichage_ligne )
        
        ligne_init = False
        for x in range(TAILLE_PLATEAU):
            pygame_x = pygame_x0 + pygame_taille_case * (x + 1) + pygame_delta * x

            # "0X " ou "XX " : Initialisaiton des positions à gauche des lignes.
            if not ligne_init:
                position = dizaine(y + 1)
                print( marge_num_x_debut + position, end = marge_num_x_fin )

                ligne_init = True

            lettre = plt_jetons[y][x]
            bonus = plt_bonus[y][x]
            draw_case(screen, pygame_taille_case, pygame_taille_font, pygame_x, pygame_y, case_color[bonus], lettre)
            
            case = " " + lettre
            if lettre != " " and bonus != "":
                case += bonus_to_symbole[bonus]
            else:
                case += " "

            affichage_case = espace_y + case
            # "| A*" ou "|   " ou "| A "
            print( affichage_case, end = "" )

        # "|\n" : Fin de ligne complétée
        print( espace_y )

    # "   |---|---|---|---|---|" : Fin du plateau
    print( affichage_ligne )

    # PyGame Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        time.sleep(1)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    """

    Q5) Programme Principal.
    A noter qu'on peut s'amuser à faire varier la TAILLE_MARGE, TAILLE_PLATEAU et autres variables (graphique ou non) comme nous le souhaitons SANS
    AUCUN PROBLEME D'AFFICHAGE à condition de modifier init_bonus() pour avoir la liste itérable.
    
    """
    # print( init_bonus() )
    jetons = init_jetons()

    affiche_jetons_q6(jetons)
