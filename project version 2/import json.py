import json
import os

def charger_bibliotheque(nom_fichier):
    if os.path.exists(nom_fichier):
        with open(nom_fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_bibliotheque(biblio, nom_fichier):
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(biblio, f, indent=4, ensure_ascii=False)

def generer_id(biblio):
    return max((livre["ID"] for livre in biblio), default=0) + 1

def afficher_livres(biblio):
    for livre in biblio:
        print(f"[{livre['ID']}] {livre['Titre']} - {livre['Auteur']} ({livre['Année']}) - {'Lu ✅' if livre['Lu'] else 'Non lu ❌'}")
        if livre['Lu']:
            print(f"  Note : {livre['Note']} | Commentaire : {livre['Commentaire']}")

def ajouter_livre(biblio):
    titre = input("Titre : ")
    auteur = input("Auteur : ")
    annee = input("Année : ")
    livre = {
        "ID": generer_id(biblio),
        "Titre": titre,
        "Auteur": auteur,
        "Année": int(annee),
        "Lu": False,
        "Note": None,
        "Commentaire": ""
    }
    biblio.append(livre)
    print("Livre ajouté ✅")

def marquer_lu(biblio):
    try:
        id_livre = int(input("ID du livre à marquer comme lu : "))
        for livre in biblio:
            if livre["ID"] == id_livre:
                livre["Lu"] = True
                livre["Note"] = int(input("Note sur 10 : "))
                livre["Commentaire"] = input("Commentaire : ")
                print("Livre mis à jour ✅")
                return
        print("Livre non trouvé ❌")
    except:
        print("Entrée invalide ❌")

def supprimer_livre(biblio):
    try:
        id_livre = int(input("ID à supprimer : "))
        for livre in biblio:
            if livre["ID"] == id_livre:
                biblio.remove(livre)
                print("Livre supprimé 🗑")
                return
        print("Livre non trouvé ❌")
    except:
        print("Entrée invalide ❌")

def menu():
    session = input("Nom de la session (ex: programmation) : ")
    fichier = f"{session}.json"
    biblio = charger_bibliotheque(fichier)

    while True:
        print("\n1. Afficher les livres")
        print("2. Ajouter un livre")
        print("3. Marquer un livre comme lu")
        print("4. Supprimer un livre")
        print("5. Quitter et sauvegarder")
        choix = input("Choix : ")

        if choix == '1':
            afficher_livres(biblio)
        elif choix == '2':
            ajouter_livre(biblio)
        elif choix == '3':
            marquer_lu(biblio)
        elif choix == '4':
            supprimer_livre(biblio)
        elif choix == '5':
            sauvegarder_bibliotheque(biblio, fichier)
            print("Bibliothèque sauvegardée ✅")
            break
        else:
            print("Choix invalide ❌")

if __name__ == "__main__":
    menu()
