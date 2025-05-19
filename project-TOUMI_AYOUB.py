import json
import os

FICHIER = "bibliotheque_TOUMI.json"

def charger_bib():
    if os.path.exists(FICHIER):
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_bib(bibliotheque):
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)

def generer_id(bibliotheque):
    if not bibliotheque:
        return 1
    return max(livre["ID"] for livre in bibliotheque) + 1

def afficher_livres(bibliotheque):
    if not bibliotheque:
        print("📚 Aucune entrée dans la bibliothèque.")
        return
    for livre in bibliotheque:
        statut = "✅ Lu" if livre["Lu"] else "❌ Non lu"
        print(f"[{livre['ID']}] {livre['Titre']} - {livre['Auteur']} ({livre['Annee']}) | {statut}")
        if livre["Lu"]:
            print(f"   Note : {livre.get('Note', 'Aucune')} | Commentaire : {livre.get('Commentaire', '')}")

def ajouter_livre(bibliotheque):
    titre = input("Titre du livre : ")
    auteur = input("Auteur : ")
    try:
        annee = int(input("Année de publication : "))
    except ValueError:
        print("⚠️ Veuillez entrer une année valide.")
        return
    nouveau_livre = {
        "ID": generer_id(bibliotheque),
        "Titre": titre,
        "Auteur": auteur,
        "Annee": annee,
        "Lu": False,
        "Note": None,
        "Commentaire": ""
    }
    bibliotheque.append(nouveau_livre)
    sauvegarder_bib(bibliotheque)
    print("✅ Livre ajouté avec succès.")

def supprimer_livre(bibliotheque):
    try:
        id_suppr = int(input("ID du livre à supprimer : "))
    except ValueError:
        print("⚠️ ID invalide.")
        return
    for livre in bibliotheque:
        if livre["ID"] == id_suppr:
            confirmation = input(f"Êtes-vous sûr de vouloir supprimer '{livre['Titre']}' ? (o/n) : ")
            if confirmation.lower() == 'o':
                bibliotheque.remove(livre)
                sauvegarder_bib(bibliotheque)
                print("🗑 Livre supprimé.")
            return
    print("❌ Livre non trouvé.")

def rechercher_livre(bibliotheque):
    mot_cle = input("Mot-clé à rechercher (titre ou auteur) : ").lower()
    resultats = [
        livre for livre in bibliotheque
        if mot_cle in livre["Titre"].lower() or mot_cle in livre["Auteur"].lower()
    ]
    if resultats:
        afficher_livres(resultats)
    else:
        print("🔍 Aucun résultat trouvé.")

def marquer_comme_lu(bibliotheque):
    try:
        id_livre = int(input("ID du livre lu : "))
    except ValueError:
        print("⚠️ ID invalide.")
        return
    for livre in bibliotheque:
        if livre["ID"] == id_livre:
            livre["Lu"] = True
            try:
                note = int(input("Note sur 10 : "))
                if not 0 <= note <= 10:
                    raise ValueError
            except ValueError:
                print("⚠️ Note invalide. Elle doit être entre 0 et 10.")
                return
            commentaire = input("Commentaire (facultatif) : ")
            livre["Note"] = note
            livre["Commentaire"] = commentaire
            sauvegarder_bib(bibliotheque)
            print("📖 Livre marqué comme lu.")
            return
    print("❌ Livre non trouvé.")

def filtrer_lus(bibliotheque, lu=True):
    livres_filtres = [livre for livre in bibliotheque if livre["Lu"] == lu]
    if livres_filtres:
        afficher_livres(livres_filtres)
    else:
        print("📚 Aucun livre correspondant.")

def trier_livres(bibliotheque):
    print("Trier par : 1. Année  2. Auteur  3. Note")
    choix = input("Votre choix : ")
    if choix == '1':
        livres_tries = sorted(bibliotheque, key=lambda x: x["Annee"])
    elif choix == '2':
        livres_tries = sorted(bibliotheque, key=lambda x: x["Auteur"].lower())
    elif choix == '3':
        livres_tries = sorted(bibliotheque, key=lambda x: (x["Note"] is None, x["Note"]))
    else:
        print("❌ Choix invalide.")
        return
    afficher_livres(livres_tries)

def menu():
    bibliotheque = charger_bib()
    while True:
        print("\n=== 📚 MENU BIBLIOTHÈQUE ===")
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
            afficher_livres(bibliotheque)
        elif choix == '2':
            ajouter_livre(bibliotheque)
        elif choix == '3':
            supprimer_livre(bibliotheque)
        elif choix == '4':
            rechercher_livre(bibliotheque)
        elif choix == '5':
            marquer_comme_lu(bibliotheque)
        elif choix == '6':
            filtrer_lus(bibliotheque, lu=True)
        elif choix == '7':
            filtrer_lus(bibliotheque, lu=False)
        elif choix == '8':
            trier_livres(bibliotheque)
        elif choix == '9':
            print("💾 Bibliothèque sauvegardée. À bientôt !")
            break
        else:
            print("❌ Option invalide.")

if __name__ == "__main__":
    menu()