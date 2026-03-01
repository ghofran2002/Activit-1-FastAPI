# Importation de la classe FastAPI pour créer l'application API
# Importation de HTTPException pour gérer les erreurs HTTP personnalisées
from fastapi import FastAPI, HTTPException

# Importation du middleware CORS pour autoriser les requêtes venant d'autres origines (ex: Angular)
from fastapi.middleware.cors import CORSMiddleware

# Importation de BaseModel pour créer des modèles de données avec validation automatique
from pydantic import BaseModel

# Importation du type List pour typer les listes
from typing import List


# Création de l'instance principale de l'application FastAPI
app = FastAPI()


# Liste des origines autorisées à accéder à l’API (ici une application Angular en local)
origins = [
    "http://localhost:4200",
]


# Ajout du middleware CORS à l'application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Autorise uniquement les origines définies ci-dessus
    allow_credentials=True,       # Autorise l'envoi des cookies / headers d’authentification
    allow_methods=["*"],          # Autorise toutes les méthodes HTTP (GET, POST, DELETE, etc.)
    allow_headers=["*"],          # Autorise tous les headers
)


# Définition du modèle Article qui décrit la structure d’un article
class Article(BaseModel):
    id: int                # Identifiant unique de l'article
    nom: str               # Nom de l'article
    description: str       # Description de l'article
    prix: float            # Prix de l'article
    en_stock: bool         # Indique si l'article est disponible en stock


# Création d'une liste typée contenant des objets Article (base de données simulée en mémoire)
catalogue: List[Article] = [
    # Premier article initialisé
    Article(id=1, nom="Coque iPhone 14", description="Coque anti-choc", prix=19.99, en_stock=True),

    # Deuxième article initialisé
    Article(id=2, nom="Chargeur USB-C", description="Charge rapide 20W", prix=15.49, en_stock=True),
]


# Route GET à la racine "/" de l’API
@app.get("/")
def root():
    # Retourne un message simple pour vérifier que l’API fonctionne
    return {"message": "API Catalogue"}


# Route GET pour récupérer la liste des articles
# response_model=List[Article] indique que la réponse sera une liste d’objets Article
@app.get("/articles/", response_model=List[Article])
def get_articles():
    # Retourne le catalogue complet
    return catalogue


# Route POST pour ajouter un nouvel article
# response_model=Article indique que la réponse sera un objet Article
# status_code=201 signifie "Créé avec succès"
@app.post("/articles/", response_model=Article, status_code=201)
def add_article(article: Article):

    # Vérifie si un article avec le même ID existe déjà
    if any(existing_article.id == article.id for existing_article in catalogue):
        # Si oui, on déclenche une erreur HTTP 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Un article avec cet ID existe déjà")

    # Ajoute le nouvel article au catalogue
    catalogue.append(article)

    # Retourne l'article ajouté
    return article


# Route DELETE pour supprimer un article selon son ID
@app.delete("/articles/{article_id}")
def delete_article(article_id: int):

    # Parcours du catalogue avec l’index pour pouvoir supprimer un élément
    for index, article in enumerate(catalogue):

        # Si l'ID correspond
        if article.id == article_id:

            # Suppression de l'article dans la liste
            del catalogue[index]

            # Retourne un message de confirmation
            return {"message": "Article supprimé"}

    # Si aucun article n'est trouvé, on retourne une erreur 404 (Not Found)
    raise HTTPException(status_code=404, detail="Article introuvable")