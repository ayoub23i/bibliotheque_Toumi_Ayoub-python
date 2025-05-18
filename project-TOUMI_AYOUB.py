import json
import os

FICHIER = "bibliothéque_TOUMI.json"



def charger_bib():

    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_bib(bibliothéque):
    with open(FICHIER, "w", encoding="utf-8") as f:                #W pour Write et R for read ,on ouvre le ficher json pour ecrire 
        json.dump(bibliothéque, f, indent=4, ensure_ascii=False)
# j'ai utiliser ici la façon la plus commune pour eviter la redandance de l'indetifcateur ,on ajout +1 chaque fois en ajouter un livree
def generer_id(bibliothéque):
    if not bibliothéque:
        return 1
    return max(livre["ID"] for livre in bibliothéque) + 1


def afficher_livres(bibliothéque):
    if not bibliothéque:
        print("📚 Aucune entree dans la bibliotheque.")
        return
    for livre in bibliothéque:
        statut = "✅ Lu" if livre["Lu"] else "❌ Non lu"
        print(f"[{livre['ID']}] {livre['Titre']} - {livre['Auteur']} ({livre['Annee']}) | {statut}")
        if livre["Lu"]:
            print(f"   Note : {livre.get('Note', 'Aucune')} | Commentaire : {livre.get('Commentaire', '')}")

def ajouter_livre(bibliothéque):
    titre = input("Titre du livre : ")
    auteur = input("Auteur : ")
    try:    #ajouter try to avoid the error in the code if the user added a wrong entry
        année = int(input("Annee de publication : "))
    except ValueError:
        print("⚠️ Veuillez entrer une annee valide.")
        return
    nouveau_livre = {
        "ID": generer_id(bibliothéque),
        "Titre": titre,
        "Auteur": auteur,
        "Annee": année,
        "Lu": False,
        "Note": None,
        "Commentaire": ""
    }
    bibliothéque.append(nouveau_livre)
    print("✅ Livre ajoute avec succes.")

def supprimer_livre(bibliothéque):
    try:
        id_suppr = int(input("ID du livre à supprimer : "))
    except ValueError:
        print("⚠️ ID invalide.")
        return
    for livre in bibliothéque:
        if livre["ID"] == id_suppr:
            confirmation = input(f"Êtes-vous sûr de vouloir supprimer '{livre['Titre']}' ? (o/n) : ")
            if confirmation.lower() == 'o':    # update the lettre to maniscule et comparer avec o ,si oui suprimer
                bibliothéque.remove(livre)
                print("🗑 Livre supprime.")
            return
    print("❌ Livre non trouve.")

def rechercher_livre(bibliothéque):
    mot_cle = input("Mot-cle a rechercher (titre ou auteur) : ").lower()
    resultats = [
        livre for livre in bibliothéque
        if mot_cle in livre["Titre"].lower() or mot_cle in livre["Auteur"].lower()    #in c'est a dire que si un mot se trouve dans la phrase afiche le (pas tout la phrase)
    ]
    if resultats:
        afficher_livres(resultats)
    else:
        print("🔍 Aucun resultat trouve.")

def marquer_comme_lu(bibliothéque):
    try:
        id_livre = int(input("ID du livre lu : "))
    except ValueError:
        print("⚠️ ID invalide.")
        return
    for livre in bibliothéque:
        if livre["ID"] == id_livre:
            livre["Lu"] = True
            try:                        
                note = int(input("Note sur 10 : "))
                if not 0 <= note <= 10:
                    raise ValueError
            except ValueError:
                print("⚠️ Note invalide. Elle doit être entre 0 et 10.")
                return
            
            #si marquer comme lu directement l'utilisateur doit ajouter un commentaire
            commentaire = input("Commentaire (facultatif) : ")
            livre["Note"] = note
            livre["Commentaire"] = commentaire
            print("📖 Livre marque comme lu.")
            return
    print("❌ Livre non trouve.")

def filtrer_lus(bibliothéque, lu=True):
    livres_filtres = [livre for livre in bibliothéque if livre["Lu"] == lu]    #filtrer la liste en fonction de la valuer j'ai appliquer le syntax dans la documantation https://docs.python.org/fr/3/tutorial/datastructures.html#list-comprehensions
    if livres_filtres:
        afficher_livres(livres_filtres)
    else:
        print("📚 Aucun livre correspondant.")

def trier_livres(bibliothéque):
    print("Trier par : 1. Annee  2. Auteur  3. Note")
    choix = input("Votre choix : ")
    if choix == '1':
        livres_tries = sorted(bibliothéque, key=lambda x: x["Annee"])
    elif choix == '2':
        livres_tries = sorted(bibliothéque, key=lambda x: x["Auteur"].lower())
    elif choix == '3':
        livres_tries = sorted(bibliothéque, key=lambda x: (x["Note"] is None, x["Note"]))
    else:
        print("❌ Choix invalide.")
        return
    afficher_livres(livres_tries)



def menu():
    bibliothéque = charger_bib()
    while True:
        print("\n=== 📚 MENU BIBLIOTHEQUE ===")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer un livre comme lu")
        print("6. Afficher les livres lus")
        print("7. Afficher les livres non lus")
        print("8. Trier les livres")
        print("9. Quitter")
        choix = input("Choisissez une option : ")

        if choix == '1':
            afficher_livres(bibliothéque)
        elif choix == '2':
            ajouter_livre(bibliothéque)
        elif choix == '3':
            supprimer_livre(bibliothéque)
        elif choix == '4':
            rechercher_livre(bibliothéque)
        elif choix == '5':
            marquer_comme_lu(bibliothéque)
        elif choix == '6':
            filtrer_lus(bibliothéque, lu=True)
        elif choix == '7':
            filtrer_lus(bibliothéque, lu=False)
        elif choix == '8':
            trier_livres(bibliothéque)
        elif choix == '9':
            sauvegarder_bib(bibliothéque)
            print("💾 Bibliotheque sauvegardee. À bientôt !")
            break
        else:
            print("❌ Option invalide.")

if __name__ == "__main__":
    menu()