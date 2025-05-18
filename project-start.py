import json
import os

FICHIER = "bibliotheque_TOUMI_AYOUB.json"



def charger_bib():

    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_bib(bibliotheque):
    with open(FICHIER, "w", encoding="utf-8") as f:                #W pour Write et R for read ,on ouvre le ficher json pour ecrire 
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)
# j'ai utiliser ici la façon la plus commune pour eviter la redandance de l'indetifcateur ,on ajout +1 chaque fois en ajouter un livree
def generer_id(bibliotheque):
    if not bibliotheque:
        return 1
    return max(livre["ID"] for livre in bibliotheque) + 1
