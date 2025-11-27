#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_LISENA_TIXIER_projet_V5.py : CR projet « srabble », groupe 032

LISENA <Enzo.Lisena@etu-univ-grenoble-alpes.fr>
TIXIER <Julien.Tixer@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from Dependances.scrabble_v1 import *
from Dependances.scrabble_v2 import *
from Dependances.scrabble_v3 import *
from Dependances.scrabble_v4 import *

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel

# PARTIE 5 : PREMIER PROGRAMME PRINCIPAL #############################################

def tour_joueur(plt, sac, infos_joueur):
    """
    
    - Préconditions: 
        * "plt" & "sac" -> list ;
        * "infos_joueur" -> dict ;
    - Postcondition: //

    Q25) Gère le tour d'un joueur en lui proposant de proposer une lettre, de passer son tour ou de faire un échange

    """
    print("- Le plateau:")
    affiche_jetons_q4(plt)

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
        # Filtre pour savoir si le mot existe et est jouable
        mot = input("[PROPOSITION] Effectue une proposition de mot correct et jouable : ('' pour arreter) ")
        while mot != "" and ( mot == "" or (mot.upper() not in dict_fr) or (not mot_jouable(mot, main)) ):
            mot = input("[PROPOSITION] Effectue une proposition de mot correct et jouable : ('' pour arreter) ")
        
        # Ajout des scores
        val_mot = valeur_mot(mot, dict_val_lettres)
        print(f"[PROPOSITION] Le mot que vous avez choisi vous rapporte {val_mot} points")

        infos_joueur[2] += val_mot
        score = infos_joueur[2]
        print(f"[PROPOSITION] Vous êtes donc à {score} points !")

        # Défaussage des mots
        for lettre in mot:
            main.remove(lettre)
        main += piocher( len(mot), sac )
        
        print(f"[NOUVELLE MAIN] {main}")

    print("[FIN DE TOUR]")

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

    numeros_joueurs = list( joueurs.keys() )
    indice = tours % nombre_joueurs
    
    return numeros_joueurs[ indice ]

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

        lettre_J1 = pioche_sans_joker(nom_J1, sac_copy)
        delta_J1 = ord(lettre_J1) - ord("A")
        
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
            liste_deltas.pop(id_J2)

            # On remet les jetons piochés dans le sac
            sac_copy.extend( [lettre_J1] * 2 )

            delta_J1, delta_J2 = refaire_jouer(nom_J1, nom_J2, liste_deltas, sac_copy)

            joueurs_deltas[id_J2] = delta_J2

        joueurs_deltas[id_J1] = delta_J1
        print()

    # TODO: Méthode de trie faite à la main avec une complexité atroce (à améliorer) LE RESTE EST GOOD ON PEUT PAS FAIRE MIEUX
    joueurs_deltas_triees = [ (num, scor) for num, scor in joueurs_deltas.items()]

    for i in range( len(joueurs_deltas_triees) ):
        position_score_mini = joueurs_deltas_triees[i]
        score_mini = position_score_mini[1]

        for j in range(i, len(joueurs_deltas_triees)):
            position_score = joueurs_deltas_triees[j]
            score = position_score[1]

            if score < score_mini:
                position_score_mini = position_score
                score_mini = score

        joueurs_deltas_triees.remove(position_score_mini)
        joueurs_deltas_triees.insert(i, position_score_mini)

    # On définit le classement final
    classement = []
    for numero, score in joueurs_deltas_triees:
        classement.append(numero)
    
    return classement

def programme_principal():
    """

    Q28)
    On définira les variables suivantes :
    - "nb_joueurs" le nombre de joueur dans la partie   ---> INT
    - "noms_joueurs" l'ensemble des noms des joueurs triés par 'indice' (qu'on appelera 'numero')   ---> LIST

    - "dico_lettres" et "sac" ...   ---> DICT

    - "joueurs" qui a comme clé le numéro du joueur, et en valeur une liste (avec son nom, sa main, son score) ---> DICT
    - "classement" une liste des numéros des joueurs, triés dans l'ordre de passage (1er jusqu'au dernier) ---> LIST

    """
    # Initialisation de toutes les valeurs créant l'état des joueurs
    nb_joueurs = int( input("[CREATION] Nombre de joueurs ? ") )

    # noms_joueurs = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
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

        tour_joueur(plt, sac, joueur_infos)

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