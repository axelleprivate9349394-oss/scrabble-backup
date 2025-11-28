#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_XXXX_YYYY_projet.py : CR projet « srabble », groupe ZZZ

XXXX <prenom.nom@etu-univ-grenoble-alpes.fr>
YYYY <prenom.nom@univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import random

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

    plt_jetons = [ [" "] * TAILLE_PLATEAU for y in range(TAILLE_PLATEAU) ]

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

def affiche_jetons(j) :
    """

    - Précondition: 
        * "j" -> list ;

    - Postcondition: //

    Q4) Affichage des jetons et bonus sur le plateau de coordonnées (x, y)

    """
    # Plateau
    plt_jetons = j.copy()
    plt_bonus = init_bonus()

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
    colonnes_init = False
    for y in range(TAILLE_PLATEAU):

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

# PARTIE 2 : LA PIOCHE ########################################################

def init_pioche_alea():
    """

    - Précondition: //

    - Postcondition: 
        * "liste_alea_jetons" -> list ;

    Q7) Générer une liste aléatoire de jetons: où (A, Z) forcément une fois + 74 autres caracs majs + 2 jokers
    
    """

    # On initialisé la liste des jetons par les 2 JOKERS
    liste_alea_jetons = [JOKER] * 2

    # On récupère les 26 lettres de l'alphabet à coup sur
    for i in range(26):
        lettre = chr( ord("A") + i )
        liste_alea_jetons.append( lettre )

    # On récupère 74 autres lettres piochées aléatoirement
    for j in range(74):
        lettre_aleatoire = chr( random.randint( ord("A"), ord("Z") ) )
        liste_alea_jetons.append( lettre_aleatoire )

    # Si on souhaite randomiser 2 fois. (avec les indices = positions), notamment pour les tests
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
        # On choisit un jeton aléatoirement dans le sac
        index_rand = random.randint( 0, len(sac) - 1 )
        jeton = sac[index_rand]

        pioche.append(jeton)
        
        # On retire ce même jeton du sac
        sac.remove(jeton)
    
    return pioche

def completer_main(main, sac):
    """

    - Préconditions: 
        * "main" & "sac" -> list ;

    - Postcondition: //

    Q9) Complète la "main" du joueur pour qu'il aie 7 jetons (si possible)

    """

    # Si notre main n'est pas complété et qu'il reset des jetons, on remplie notre main une par une
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

    # S'il y a assez de jetons dans le sac, alors l'échange peut commencer
    success = len(sac) >= len(jetons)

    temp_sac = []

    i = 0
    while success and i < len(jetons):
        # On vérifie que le jeton proposé est bien dans la main, si c'est le cas, l'échange réussi
        jeton = jetons[i]
        success = jeton in main

        if success:
            main.remove(jeton)
            temp_sac.append(jeton)
        
        i += 1
    
    if success:
        # On repioche l'équivalent de jetons échangés SACHANT qu'on a pas encore remis les jetons
        # échangés dans le sac
        main += piocher( len(jetons), sac )
        sac += temp_sac
    else:
        # On redonne l'équivalent perdu
        main += temp_sac

    return success

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

    - Postcondition: 
        * "motsfr_let" -> list ;

    Q13) Renvoie tous les mots possibles du scrabble où la lettre "let" est au début du mot.

    >>> len( select_mot_initiale(generer_dictfr(), "Z") )
    229

    """

    motsfr_let = []

    for mot in motsfr:
        # On vérifie si la première lettre du mot est celle cherchée en paramètre
        if mot[0] == let.upper():
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

def mot_jouable(mot, ll, check_joker = True):
    """

    - Préconditions: 
        * "mot" -> str ; 
        * "ll" -> list ;
        * "check_joker" -> bool ; <optionnel>

    - Postcondition: 
        * "success" -> bool ;

    Q15 & 17) Permet de savoir si on peut écrire le "mot" à l'aide des lettres dans "ll" (en comptant les jokers)

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
        joker_apparait = check_joker and JOKER in temp_ll

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

    Q16) Renvoie la liste des mots qu'on peut faire avec les lettres de notre main ("ll")
    
    """
    liste_mots = []

    for mot in motsfr:

        if mot_jouable(mot, ll):
            liste_mots.append(mot)
    
    return liste_mots

# TODO : REFAIRE CORRECTEMENT
def generer_mots_jouables(lettres_main, lettres_plateau, nb_lettres_manquantes):
    """

    - Préconditions: 
        * "lettres_main" & lettres_plateau -> list ; 
        * "nb_lettres_manquantes" -> int ;

    - Postcondition: 
        * "liste_mots_jouables" -> list ;

    Q18) Genere une liste de mots jouables avec "les lettre du plateau", "les lettres de notre main" 
    avec un certain "nombre de lettres manquantes"

    """
    mots_fr = generer_dictfr()

    lgr_min = nb_lettres_manquantes
    lgr_max = len(lettres_main) + len(lettres_plateau) + nb_lettres_manquantes

    mot_lgr = []

    for lgr in range(lgr_min, lgr_max + 1):
        mot_lgr.extend(select_mot_longueur(mots_fr, lgr))

    main_totale = lettres_main + lettres_plateau + [JOKER] * nb_lettres_manquantes
    liste_mots_jouables = mots_jouables(mot_lgr, main_totale)

    return liste_mots_jouables

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
    
    - Précondition: 
        * "dico" -> dict ;

    - Postcondition: 
        * "pioche" -> list ;

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

# Fonction obsolete
# def valeur_mot(mot, dico):
#     """
    
#     - Préconditions:
#         "mot" -> str ;
#         "dico" -> dict ;
#     - Postcondition: "valeur" -> int

#     Q22) Détermine la valeur d'un "mot" en fonction des valeurs des lettres du "mot
#     >>> dico = generer_dico()

#     >>> valeur_mot("BEBE", dico)
#     8
#     >>> valeur_mot("PARADISIAQUE", dico)
#     22

#     """
#     valeur = 0
#     for lettre in mot:
#         valeur += dico[lettre]["val"]
    
#     return valeur

def meilleur_mot(motsfr, ll, dico):
    """
    - Préconditions:
        * "dico" -> dict ;
        * "motsfr" & "ll" -> list ;

    - Postcondition: 
        * "meilleur_mot" -> str ;

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

    # On détermine à l'avance la meilleure valeur
    meilleure_valeur = valeur_mot( meilleur_mot(motsfr, ll, dico), dico )

    meilleurs_mots = []

    for mot in mots:
        if valeur_mot(mot, dico) == meilleure_valeur:
            meilleurs_mots.append(mot)
            
    return meilleurs_mots

# PARTIE 5 : PREMIER PROGRAMME PRINCIPAL #############################################

# TODO: vérifier si c'est vraiment ca
def fin_de_partie(main, sac):
    """

    - Préconditions: 
        * "main" & "sac" -> list ;

    - Postcondition: 
        * "fin" -> bool ;

    Q26) Détermine si c'est la fin de la partie ou non
    >>> fin_de_partie(["A", "Z", "U"], ["P"])
    >>> True

    >>> fin_de_partie(["A", "Z", "U", "K"], ["P, "I", "Z"])
    >>> False

    """
    fin = len(sac) + len(main) < 7
    return fin

def detection_prochain_joueur(tours, joueurs):
    """
    
    - Préconditions:
        * "tours" -> int ;
        * "joueurs" -> dict ;

    - Postcondition: 
        * "joueur" -> int ;

    Q27) Détecte qui sera le prochain joueur. A noter que "joueurs" est trié de sorte
    que le joueur à la position i + 1 soit le joueur correspondant au prochain tour
    >>> joueurs = { 1: [nom_1, main_1, score_1], 0: [nom_0, main_0, score_0], 2: [nom_2, main_2, score_2] }

    >>> detection_prochain_joueur(0, joueurs)
    >>> 1

    >>> detection_prochain_joueur(4, joueurs)
    >>> 0

    """

    nombre_joueurs = len(joueurs)

    # On se permet de récupérer dans le bon ordre les "ids" / "numéros" des joueurs
    numeros_joueurs = list( joueurs.keys() )

    # On sait à l'avance qu'au tour = 0, c'est le joueur à l'indice 0 qui commence, il n'y a plus
    # qu'a créé une "périodicité" pour chaque tour
    indice = tours % nombre_joueurs
    
    return numeros_joueurs[indice]

def pioche_sans_joker(nom_joueur, sac):
    """

    - Préconditions:
        * "nom_joueur" -> str ;
        * "sac" -> list ;

    - Postcondition: 
        * "lettre" -> str ;

    Q28.bis) Permet l'affichage et la pioche d'une lettre dans le sac QUI N'EST PAS UN JOKER

    """

    lettre = piocher(1, sac)[0]
    print(f"[ORDRE PASSAGE] Le Joueur {nom_joueur} vous avez pioché : {lettre}")
    while lettre == JOKER:
        lettre = piocher(1, sac)[0]
        print(f"[ORDRE PASSAGE] Le Joueur {nom_joueur} vu que vous aviez pioché un JOKER, voici votre nouvelle lettre : {lettre}")

    return lettre

def refaire_jouer(nom_J1, nom_J2, liste_deltas, sac):
    """

    - Préconditions:
        * "nom_J1" & "nom_J2" -> str ;
        * "liste_deltas" & "sac" -> list ;

    - Postconditions: 
        * "(delta_J1, delta_J2)" -> tuple ;

    Q28.bis) Permet de refaire jouer les deux joueurs qui ont pioché la même lettre

    """
    lettre_J1 = None
    lettre_J2 = None

    # Si on arrive ici, c'est que lettre_J1 et lettre_J2 sont égales (par définition)
    lettres_egales = True
    while lettres_egales:
        # Affichage
        if lettre_J1 == lettre_J2:
            print(f"[ORDRE PASSAGE] Le Joueur {nom_J1} a pioché la même lettre que le Joueur {nom_J2}")
        else:
            print(f"[ORDRE PASSAGE] Le Joueur {nom_J1} ou {nom_J2} a pioché la même lettre qu'un autre joueur")

        # Pioche de J1
        lettre_J1 = pioche_sans_joker(nom_J1, sac)
        delta_J1 = ord(lettre_J1) - ord("A")

        # Pioche de J2
        lettre_J2 = pioche_sans_joker(nom_J2, sac)
        delta_J2 = ord(lettre_J2) - ord("A")

        # Si c'est une lettre qui a déjà été pioché, ou que c'est la même que le joueur contre qui on joue
        lettres_egales = delta_J1 in liste_deltas or delta_J2 in liste_deltas or delta_J1 == delta_J2

        # On remet les jetons dans le sac
        if lettres_egales:
            sac.extend( [lettre_J1, lettre_J2] )
    
    return (delta_J1, delta_J2)

def determine_tour(noms_joueurs, sac):
    """
    SELON LES REGLES DU SCRABBLE CLASSIQUE (c.f : https://fisf.net/scrabble/decouverte/formules-de-jeu/)

    - Préconditions:
        * "nb_joueurs" & "sac" -> list ;

    - Postcondition: 
        * "classement" -> list ;

    Q28.bis) Permet de savoir l'ordre dans lequel les joueurs vont jouer, avec
    classement qui renvoie une liste des numéros des joueurs triés dans l'ordre croissant
    (1er jusqu'à dernier)

    """
    nb_joueurs = len(noms_joueurs)
    sac_copy = sac.copy()

    joueurs_deltas = {} # on determine un "delta" avec la distance de la lettre piochée à "A" (par exemple "B" est à une distance de 1)
    
    for id_J1 in range( nb_joueurs ):
        nom_J1 = noms_joueurs[id_J1]

        # On calcule la distance de la "lettre_J1" avec la lettre "A"
        lettre_J1 = pioche_sans_joker(nom_J1, sac_copy)
        delta_J1 = ord(lettre_J1) - ord("A")
        
        # On récupère la liste des distances des anciens joueurs
        liste_deltas = list( joueurs_deltas.values() )
        
        # On parcourt "liste_deltas" pour voir si un jeton ne s'est pas répété
        id_J2 = 0
        doublon = False
        while id_J2 < len(liste_deltas) and not doublon:
            doublon = delta_J1 == liste_deltas[id_J2]

            if not doublon:
                id_J2 += 1

        # Si un autre joueur a aussi pioché cette lettre on refait piocher les deux jusqu'à qu'ils aient des lettres différentes
        if doublon:
            nom_J2 = noms_joueurs[id_J2]
            # On retire bien la "distance" de la lettre piochée par le J2
            liste_deltas.pop(id_J2)

            # On remet les jetons piochés dans le sac
            sac_copy.extend( [lettre_J1] * 2 )

            # On refait jouer jusqu'à que les lettres soient différentes entre elles et de celles du sac
            delta_J1, delta_J2 = refaire_jouer(nom_J1, nom_J2, liste_deltas, sac_copy)

            joueurs_deltas[id_J2] = delta_J2

        joueurs_deltas[id_J1] = delta_J1
        print()

    # Tri par sélection ( ATTENTION C'EST UN PEU ABSTRAIT, juste un peu beaucoup :) )
    liste_numeros = list( joueurs_deltas.keys() )
    liste_deltas = list( joueurs_deltas.values() )

    for i in range( len(liste_numeros) - 1 ):
        # On initialise le "delta_mini"
        delta_mini = liste_deltas[i]
        indice_mini = i

        # On cherche le "delta_mini" dans le reste de la liste non triée
        for j in range( i + 1, len(liste_numeros) ):
            delta = liste_deltas[j]

            if delta < delta_mini:
                delta_mini = delta
                indice_mini = j

        # On échange les deux éléments afin d'avoir la partie triée à gauche de la liste (on s'assure d'avoir les couples numéros et deltas au même indice)
        # même s'ils sont dans deux listes différentes ON NE VEUT SURTOUT PAS PERDRE L'ASSOCIATIVITE (NUMERO, DELTA)
        liste_numeros[i], liste_numeros[indice_mini] = liste_numeros[indice_mini], liste_numeros[i] # Numéros
        liste_deltas[i], liste_deltas[indice_mini] =  liste_deltas[indice_mini], liste_deltas[i]    # Deltas

    # On définit le classement final
    classement = []
    for numero in liste_numeros:
        classement.append(numero)
    
    return classement

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
    # while (x < 1 or x > TAILLE_PLATEAU) or (y < 1 or y > TAILLE_PLATEAU):
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
        # Faire petit dessin pour comprendre
        parcourt_droite = TAILLE_PLATEAU - i - len(mot) >= 0
        ligne = plateau[j]

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

def placer_mot(plateau, lm, mot, i, j, dir, dict_fr):
    """

    - Préconditions:
        * "plateau" & "lm" -> list ;
        * "i" & "j" -> int ;
        * "dir" & "mot" -> str ;
        * "dict_fr" -> dict ;

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

    plateau_copy = plateau.copy()
    lm_utilisees = []

    liste_lettres = tester_placement(plateau, i, j, dir, mot)

    horizontal = dir == "horizontal"
    vertical = dir == "vertical"

    # vérifier que les élé de liste_lettres sont dans lm
    success = liste_lettres != []
    k = 0
    while success and k < len(liste_lettres):
        lettre = liste_lettres[k]
        success = success and lettre in lm
        if success:
            liste_lettres.remove(lettre)

        k += 1
        
    # Signifie qu'on peut placer le mot ici
    if success:
        
        x, y = i, j

        collisions_horizontal_vertical = { "horizontal": [False, False], "vertical": [False, False] }

        collision_lettres = []
        for lettre in mot:
            collided_gauche, collided_droite, collided_haut, collided_bas = False, False, False, False

            # On retire l'ensemble des lettres de la main, et on les ajoute
            # à la liste des lettres utilisées si on a pas essayé de compléter un mot du plateau (si possible)
            if plateau_copy[y][x] == " ":
                if lettre in lm:
                    plateau_copy[y][x] = lettre
                    lm_utilisees.append(lettre)
                    lm.remove(lettre)

            if horizontal:
                # Vérif si il y a une lettre à gauche du début du mot
                if x == i:
                    collided_gauche = 0 <= x - 1 < TAILLE_PLATEAU and plateau_copy[y][x-1] != " "
                    collisions_horizontal_vertical[dir][0] = collided_gauche
                # Vérif si il y a une lettre à droite de la fin du mot
                elif x == i + len(mot) - 1:
                    collided_droite = 0 <= x + len(mot) - 1 < TAILLE_PLATEAU and plateau_copy[y][x + len(mot) - 1 ] != " "
                    collisions_horizontal_vertical[dir][1] = collided_droite

                # Vérif si il y a une lettre en haut de la lettre du mot
                if 0 <= y - 1 < TAILLE_PLATEAU:
                    collision_haut = plateau_copy[y-1][x] != " "
                # Vérif si il y a une lettre en bas de la lettre du mot
                if 0 <= y + 1 < TAILLE_PLATEAU:
                    collided_bas = plateau_copy[y+1][x] != " "

                collision_lettres.append( (collided_haut, collided_bas) )
                x += 1

            if vertical:
                # Vérif si il y a une lettre en haut du début du mot
                if y == j:
                    collided_haut = 0 <= y - 1 < TAILLE_PLATEAU and plateau_copy[y - 1][x] != " "
                    collisions_horizontal_vertical[dir][0] = collided_haut
                # Vérif si il y a une lettre à droite de la fin du mot
                elif y == j + len(mot) - 1:
                    collided_bas = 0 <= y + len(mot) - 1 < TAILLE_PLATEAU and plateau_copy[y + len(mot) - 1][x] != " "
                    collisions_horizontal_vertical[dir][1] = collided_bas

                if 0 <= x - 1 < TAILLE_PLATEAU:
                    collided_gauche = plateau_copy[y][x-1] != " "
                if 0 <= x + 1 < TAILLE_PLATEAU:
                    collided_droite = plateau_copy[y][x+1] != " "

                y += 1
                collision_lettres.append( (collided_gauche, collided_droite) )
        


        """
        Si le mot placé est à l'horizontal
        """
        if horizontal:
            collided_gauche, collided_droite = collisions_horizontal_vertical[dir]

            # Verification 1) : On vérifie la ligne où on a posé notre lettre
            mot_forme = mot
            if collided_gauche:
                x_mot_forme = i - 1
                while 0 <= x_mot_forme < TAILLE_PLATEAU and plateau_copy[y][x_mot_forme] != " ":
                    lettre = plateau_copy[y][x_mot_forme]
                    mot_forme = lettre + mot_forme
                    x_mot_forme -= 1

            if collided_droite:
                x_mot_forme = x
                while 0 <= x_mot_forme < TAILLE_PLATEAU and plateau_copy[y][x_mot_forme] != " ":
                    lettre = plateau_copy[y][x_mot_forme]
                    mot_forme = mot_forme + lettre
                    x_mot_forme += 1

            # On vérifie si le nouveau mot formé est bien dans le dico
            success = mot_forme in dict_fr

            # Verification 2) : On vérifie les colonnes où on a posé notre lettre forment un nouveau mot
            k = 0
            while success and k < len(mot):
                collision_haut, collision_bas = collision_lettres[k]
                x_mot_forme = i + k

                # Notre futur mot formé commencera pas la lettre du mot
                mot_forme = mot[k]

                # On vérifie le mot formé à l'aide des lettres en haut
                if collision_haut:
                    y_mot_forme = y - 1
                    while 0 <= y_mot_forme < TAILLE_PLATEAU and plateau_copy[y_mot_forme][x_mot_forme] != " ":
                        lettre = plateau_copy[y_mot_forme][x_mot_forme]
                        mot_forme = lettre + mot_forme
                        y_mot_forme -= 1

                # On vérifie le mot formé à l'aide des lettres en haut et en bas ou que en bas (selon ce sur quoi on est tombé en haut)
                if collision_bas:
                    y_mot_forme = y + 1
                    while 0 <= y_mot_forme < TAILLE_PLATEAU and plateau_copy[y_mot_forme][x_mot_forme] != " ":
                        lettre = plateau_copy[y_mot_forme][x_mot_forme]
                        mot_forme = mot_forme + lettre
                        y_mot_forme += 1

                # Si on a formé un mot à l'aide des lettres du dessus ou d'en bas, on cherche
                # à savoir si ce mot est correct
                if collision_bas or collided_haut:
                    success = mot_forme in dict_fr
                
                k += 1



        """
        Si le mot placé est à la verticale, on effectue la meme chose que pour l'horizontal,
        sauf qu'ici les indices ne sont pas les memes
        """
        if vertical:
            collided_haut, collided_bas = collisions_horizontal_vertical[dir]

            # Verification 1) : On vérifie si les lettres qu'on a posé forment un nouveau mot composés des lettres d'en haut ou en bas
            mot_forme = mot
            if collided_haut:
                y_mot_forme = j - 1
                while 0 <= y_mot_forme < TAILLE_PLATEAU and plateau_copy[y_mot_forme][x] != " ":
                    lettre = plateau_copy[y_mot_forme][x]
                    mot_forme = lettre + mot_forme
                    y_mot_forme -= 1

            if collided_bas:
                y_mot_forme = y
                while 0 <= y_mot_forme < TAILLE_PLATEAU and plateau_copy[y_mot_forme][x] != " ":
                    lettre = plateau_copy[y_mot_forme][x]
                    mot_forme = mot_forme + lettre
                    y_mot_forme += 1

            # On vérifie si le nouveau mot formé est bien dans le dico
            success = mot_forme in dict_fr

            # Verification 2) : On vérifie si les lettres qu'on a posé forment un nouveau mot à leur gauche, ou leur droite
            k = 0
            while success and k < len(mot):
                collision_gauche, collision_droite = collision_lettres[k]
                y_mot_forme = j + k

                # Notre futur mot formé commencera par la lettre du mot à l'emplacement "k"
                mot_forme = mot[k]

                # On créé le mot formé à l'aide des lettres à gauche
                if collision_gauche:
                    x_mot_forme = x - 1
                    while 0 <= x_mot_forme < TAILLE_PLATEAU and plateau_copy[y_mot_forme][x_mot_forme] != " ":
                        lettre = plateau_copy[y_mot_forme][x_mot_forme]
                        mot_forme = lettre + mot_forme
                        x_mot_forme -= 1

                # On créé le mot formé à l'aide des lettres à gauche et à droite ou que à gauche (selon ce sur quoi on est tombé à gauche)
                if collision_droite:
                    x_mot_forme = x + 1
                    while 0 <= x_mot_forme < TAILLE_PLATEAU and plateau_copy[y_mot_forme][x_mot_forme] != " ":
                        lettre = plateau_copy[y_mot_forme][x_mot_forme]
                        mot_forme = mot_forme + lettre
                        x_mot_forme += 1

                # Si on a formé un mot à l'aide des lettres de gauche ou de droite, on cherche
                # à savoir si ce mot est correct
                if collision_gauche or collision_droite:
                    success = mot_forme in dict_fr
                
                k += 1

    # Si c'est OK, on update le plateau
    if success:
        plateau = plateau_copy.copy()

    # Sinon, on remet les lettres utilisées dans la main du joueur
    else:
        lm += lm_utilisees

    return success

def valeur_mot(plateau, plateau_bonus, positions_depart, direction, mot, dico):
    """
    
    - Préconditions:
        * "plateau" & "plateau_bonus" -> list ;
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

    # Exemple: on a placé "VALEUR" à l'horizontal on note:
    # cases = [" V*", " A ", ...]
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
    case_to_multiplicateur = {        
        "MT": 3,     # MOT TRIPLE
        "MD": 2,     # MOT DOUBLE
        
        "LT": 3,  # LETTRE TRIPLE
        "LD": 2   # LETTRE DOUBLE
    }

    multiplicateur_mot = 1
    valeur_mot = 0

    horizontal = direction == "horizontal"
    vertical = direction == "vertical"

    x, y = positions_depart

    for i in range( len(mot) ):
        lettre = plateau[y][x]
        case = plateau_bonus[y][x]

        multiplicateur_lettre = 1

        # On se permet un niveau d'abstraction un peu plus élevé en appliquant directement
        # le bonus si c'est une lettre ou un mot (grace à la premiere lettre du bonus)
        if case != "":
            est_lettre = case[0] == "L"

            # Si c'est un multiplicateur de lettre
            if est_lettre:
                multiplicateur_lettre = case_to_multiplicateur[case]
            # Si c'est un multiplicateur de mot TODO : si y'en a deux ?!
            else:
                multiplicateur_mot = case_to_multiplicateur[case]
            
            # On réinitialise la case bonus
            plateau_bonus[y][x] = ""

        valeur_mot += dico[lettre]["val"] * multiplicateur_lettre

        # Incrémentation
        if horizontal:
            x += 1
        elif vertical:
            y += 1

    valeur_mot *= multiplicateur_mot
    
    return valeur_mot

# PARTIE 7 : PROGRAMME PRINCIPAL FINAL ###################################################

def get_lettres_plateau(plateau):
    lettres = []

    for y in range(TAILLE_PLATEAU):
        for x in range(TAILLE_PLATEAU):
            lettre = plateau[y][x]

            if lettre not in lettres:
                lettres.append(lettre)
    
    return lettres

def tour_joueur(plt, plt_bonus, sac, infos_joueur):
    """
    
    - Préconditions: 
        * "plt" & "plt_bonus" & "sac" -> list ;
        * "infos_joueur" -> dict ;
        
    - Postcondition: //

    Q34) Gère le tour d'un joueur en lui proposant de proposer une lettre, de passer son tour ou de faire un échange

    """
    dict_fr = generer_dictfr()
    dict_val_lettres = generer_dico()

    echange_possible = len(sac) >= 7

    main = infos_joueur[1]
    print(f"[MAIN] {main}")

    # Gestion des réponses possibles
    reponse = None
    while reponse not in ["pa", "e", "pr"] or (reponse == "e" and not echange_possible):
        if not echange_possible:
            reponse = input("- passer [pa], proposer [pr] : ").lower()
        else:
            reponse = input("- passer [pa], échanger [e], proposer [pr] : ").lower()

    # Cas échange
    if reponse == "e":
        main = infos_joueur[1]

        echange_reussi = False
        while not echange_reussi:

            jetons_changer = []
            jeton_changer = input(f"[ECHANGE] Quelles jetons veux tu échanger? ('stop' pour arreter) ")
            while jeton_changer != "stop":
                jetons_changer.append(jeton_changer)

                jeton_changer = input(f"[ECHANGE] Quelles jetons veux tu échanger? ('stop' pour arreter) ")
            
            echange_reussi = echanger(jetons_changer, main, sac)

            if echange_reussi:
                infos_joueur[1] = main
                nouvelle_main = infos_joueur[1]

                print("[ECHANGE] Echange REUSSI")
                print(f"[NOUVELLE MAIN] {nouvelle_main}")
            else:
                print("[ECHANGE] Echange LOUPE")

    # Cas proposition
    elif reponse == "pr":
        
        mot_bien_place = False
        while not mot_bien_place:

            # Filtre pour savoir si le mot existe et est jouable
            mot_correct = False
            while not mot_correct:

                # DEBUT D'IA
                lettres_plateau = get_lettres_plateau(plt)
                liste_mots_jouables = generer_mots_jouables(main, lettres_plateau, 0)
                if liste_mots_jouables != []:
                    print(f"[AIDE] Mot possible à jouer {liste_mots_jouables[random.randint(0, len(liste_mots_jouables)-1)]}")
                    
                mot = input("[PROPOSITION] Effectue une proposition de mot correct et jouable : ('' pour arreter) ")

                # GESTION DU CAS OU IL Y A UN JOKER
                mot_sans_joker = ""
                nb_jokers = 0
                for lettre in mot:
                    if lettre == JOKER:
                        nb_jokers += 1
                        lettre = input(f"[PROPOSITION] JOKER n°{nb_jokers} Nous avons remarqué que vous avez utilisé un JOKER? En quelle lettre souhaitez vous le transformer? (ATTENTION CETTE TRANSFORMATION EST DEFINITIVE) ")
                        while not ("A" <= lettre <= "Z"):
                            lettre = input(f"[PROPOSITION] JOKER n°{nb_jokers} Nous avons remarqué que vous avez utilisé un JOKER? En quelle lettre souhaitez vous le transformer? (ATTENTION CETTE TRANSFORMATION EST DEFINITIVE) ")
                        
                        main.remove(JOKER)
                        main.append(lettre)
                    mot_sans_joker += lettre

                mot_correct = mot_sans_joker.upper() in dict_fr and mot_sans_joker in liste_mots_jouables

            # Définie la direction
            direction = None
            while direction not in ['horizontal', 'vertical']:
                direction = input(" 'horizontal' ou 'vertical' ? ")

            # Définie la position du mot
            x, y = lire_coords()
            x -= 1
            y -= 1

            mot_bien_place = placer_mot(plt, main, mot_sans_joker, x, y, direction, dict_fr)

        # Ajout des scores
        val_mot = valeur_mot(plt, plt_bonus, (x, y), direction, mot, dict_val_lettres)

        print(f"[PROPOSITION] Le mot que vous avez choisi vous rapporte {val_mot} points")

        infos_joueur[2] += val_mot
        score = infos_joueur[2]
        print(f"[PROPOSITION] Vous êtes donc à {score} points !")

        # On repioche les lettres
        completer_main(main, sac)
        
        print(f"[NOUVELLE MAIN] {main}")

    print("[FIN DE TOUR]")

def programme_principal():
    # Initialisation de toutes les valeurs créant l'état des joueurs
    nb_joueurs = int( input("[CREATION] Nombre de joueurs ? ") )

    noms_joueurs = []
    for i in range(1, nb_joueurs + 1):

        # Vérifie que tous les joueurs ont des noms différents
        nom_joueur = input(f"[CREATION] Joueur n°{i} : Quelle est votre nom ? ")
        while nom_joueur in noms_joueurs:
            print("[CREATION ERREUR] Vous avez pris le même nom qu'un autre joueur!")
            nom_joueur = input(f"[CREATION] Joueur n°{i} : Quelle est votre nom ? ")

        noms_joueurs.append( nom_joueur )
    print()

    # Déterminons l'ordre de passage
    dico_lettres = generer_dico()
    sac = init_pioche(dico_lettres)

    print("[CREATION] Nous allons désormais déterminer l'odre de passage !")
    classement = determine_tour(noms_joueurs, sac)

    # Initialisation des joueurs selon leur ordre de passage
    joueurs = {}
    for position in range( len(classement) ):
        id_joueur = classement[position]

        nom_joueur = noms_joueurs[id_joueur]
        main_joueur = piocher(7, sac)

        print(f"[CLASSEMENT] Le Joueur {nom_joueur} commence en position {position + 1}")

        joueurs[ id_joueur ] = [nom_joueur, main_joueur, 0]

    print("[FIN DE CREATION] Tous les jetons piochés pendant l'ordre de passage ont été remis dans le sac")
    print()

    plt = init_jetons()
    plt_bonus = init_bonus()

    # On fait tourner la partie (boucle principale)
    tour = 0
    fin_partie = False
    while not fin_partie:
        prochain_numero_joueur = detection_prochain_joueur(tour, joueurs)
        joueur_infos = joueurs[ prochain_numero_joueur ]

        nom = joueur_infos[0]
        main = joueur_infos[1]
        score = joueur_infos[2]

        print(f"[JEU TOUR n°{tour}] Au tour de {nom} | SCORE {score} |")

        print("- Le plateau:")
        affiche_jetons(plt)

        tour_joueur(plt, plt_bonus, sac, joueur_infos)

        score = joueur_infos[2]
        print(f"[FIN TOUR] {nom} Vous finissez avec un score | SCORE {score} |")
        print()

        fin_partie = fin_de_partie(main, sac)
        tour += 1
    
    # On détermine le gagnant
    gagnant = None
    score_maxi = 0
    for joueur_infos in joueurs.values():
        nom = joueur_infos[0]
        main = joueur_infos[1]

        # Calcul des malus
        malus = 0
        for lettre in main:
            malus += valeur_mot(lettre, dico_lettres)
        joueur_infos[2] -= malus
        
        score = joueur_infos[2]
        print(f"[SCORE] Le Joueur: {nom} a fini avec {score} points !")

        # On départage le gagnant (si égalité) avec l'ordre de passage déterminé au début pour éviter les confusions.
        if score > score_maxi:
            score_maxi = score
            gagnant = nom

    print()
    print(f"[WINNER] Le grand gagnant est donc {gagnant} avec un total de {score_maxi} points !")

if __name__ == "__main__":
    programme_principal()