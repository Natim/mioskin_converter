# -*- coding: utf-8 -*-
import csv
import os
import sys

MIOSKIN = True    # True | False
SCDB = True       # True | False
HAUTEUR = True    # True | False
SURCHARGE = True  # True | False

DELIMITEUR_SORTIE = ','  # ',' | ';'

# Construction du nom du fichier de sortie (on remplace l'extension par .csv
fichier_entree = sys.argv[1]
fichier_sortie, ext = os.path.splitext(fichier_entree)
fichier_sortie += ".csv"


# ON OUVRE LE FICHIER D'ENTREE
with open(sys.argv[1], newline='', encoding='utf-8') as csv_entree:

    # ON OUVRE LE FICHIER DE SORTIE
    with open(fichier_sortie, "w", newline='',
              encoding='utf-8') as csv_sortie:

        # ON CREE UN LECTEUR de fichier CSV
        reader = csv.reader(csv_entree, delimiter=',')

        # ON CREE UN ECRIVEUR de fichier CSV
        writer = csv.writer(csv_sortie, delimiter=DELIMITEUR_SORTIE)

        first_line = True

        # POUR CHAQUE LIGNE EN ENTREE
        for row in reader:
            row = list(row)
            if first_line:
                # ON GERE LES ENTETES de COLONNES
                result = row[0:2]
                if MIOSKIN:
                    result.append("MIOSKIN")
                if SCDB:
                    result.append("SCDB")
                if HAUTEUR:
                    result.append("HAUTEUR")
                if SURCHARGE and len(row) > 6:
                    result.append("SURCHARGE")
                first_line = False

            else:
                # On LIT LES COLONNES DE LA LIGNE
                radar_type = row[2]
                speed = row[3]
                dirtype = row[4]
                direction = row[5]

                surcharge = False
                if len(row) > 6:
                    surcharge = row[6]

                result = row[0:2]

                # ON CONSTRUIT LES NOUVELLES COLONNES POUR LA LIGNE
                # mioskin
                if MIOSKIN:
                    result.append("%sD%sa%s" % (dirtype, direction, speed))

                # scdb - fixe,ecotaxe,en1 feuxen2 pn,tramway,en 3 tr en 4
                if SCDB:
                    result.append("%s-%sD%sa%s" % (radar_type, dirtype,
                                                   direction, speed))

                # pour les hauteurs en 7 ou( 82 radardroid,speed a 0)
                if HAUTEUR:
                    result.append("H%sD%sa%s" % (speed, dirtype, direction))

                if SURCHARGE and surcharge:
                    # pour les surcharges
                    result.append("SD%sa%s" % (direction, surcharge))

            # ON ECRIT LA NOUVELLE LIGNE
            writer.writerow(result)


# ON DIT QUE TOUT S'EST BIEN PASSÉE
print("OK fichier `%s` a été créé" % fichier_sortie)
