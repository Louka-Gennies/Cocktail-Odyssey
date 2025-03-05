# app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional
import os

# Configuration de la base de données
DATABASE_URL = "sqlite:///./data/cocktails.db"  # Changé pour utiliser le dossier data

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèles de données
class Cocktail(Base):
    __tablename__ = "cocktails"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    description = Column(Text)
    image = Column(String)
    recipe = Column(Text)
    user_id = Column(String, ForeignKey("users.id"))

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String)
    password = Column(String)
    name = Column(String)

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    unit = Column(String)

class CocktailIngredient(Base):
    __tablename__ = "cocktail_ingredients"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    cocktail_id = Column(String, ForeignKey("cocktails.id"))
    ingredient_id = Column(String, ForeignKey("ingredients.id"))
    quantity = Column(DECIMAL)

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    cocktail_id = Column(String, ForeignKey("cocktails.id"))

class UserIngredient(Base):
    __tablename__ = "user_ingredients"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    ingredient_id = Column(String, ForeignKey("ingredients.id"))

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    cocktail_id = Column(String, ForeignKey("cocktails.id"))
    rating = Column(DECIMAL)

# Ajoutez ces classes Pydantic pour la validation des données d'entrée
class CocktailInput(BaseModel):
    name: str
    description: str
    image: str
    recipe: str
    user_id: Optional[str] = None

class UserInput(BaseModel):
    email: str
    password: str
    name: str

class IngredientInput(BaseModel):
    name: str
    unit: str

class CocktailIngredientInput(BaseModel):
    cocktail_id: str
    ingredient_id: str
    quantity: float

class FavoriteInput(BaseModel):
    user_id: str
    cocktail_id: str

class UserIngredientInput(BaseModel):
    user_id: str
    ingredient_id: str

class RatingInput(BaseModel):
    user_id: str
    cocktail_id: str
    rating: float

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes pour récupérer, créer, modifier et supprimer les données

@app.get("/api/cocktails")
def read_cocktails():
    db = SessionLocal()
    cocktails = db.query(Cocktail).all()
    return [cocktail_to_dict(cocktail) for cocktail in cocktails]

@app.post("/api/cocktails")
def create_cocktail(cocktail_data: CocktailInput):
    db = SessionLocal()
    cocktail = Cocktail(
        name=cocktail_data.name,
        description=cocktail_data.description,
        image=cocktail_data.image,
        recipe=cocktail_data.recipe,
        user_id=cocktail_data.user_id
    )
    db.add(cocktail)
    db.commit()
    db.refresh(cocktail)
    return cocktail_to_dict(cocktail)

@app.put("/api/cocktails/{cocktail_id}")
def update_cocktail(cocktail_id: str, cocktail_data: CocktailInput):
    db = SessionLocal()
    db_cocktail = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if db_cocktail:
        db_cocktail.name = cocktail_data.name
        db_cocktail.description = cocktail_data.description
        db_cocktail.image = cocktail_data.image
        db_cocktail.recipe = cocktail_data.recipe
        db_cocktail.user_id = cocktail_data.user_id
        db.commit()
        db.refresh(db_cocktail)
    return cocktail_to_dict(db_cocktail)

@app.delete("/api/cocktails/{cocktail_id}")
def delete_cocktail(cocktail_id: str):
    db = SessionLocal()
    db_cocktail = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if db_cocktail:
        db.delete(db_cocktail)
        db.commit()
    return {"message": "Cocktail deleted successfully"}

@app.get("/api/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    return [user_to_dict(user) for user in users]

@app.post("/api/users")
def create_user(user_data: UserInput):
    db = SessionLocal()
    user = User(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_to_dict(user)

@app.put("/api/users/{user_id}")
def update_user(user_id: str, user_data: UserInput):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.email = user_data.email
        db_user.password = user_data.password
        db_user.name = user_data.name
        db.commit()
        db.refresh(db_user)
    return user_to_dict(db_user)

@app.delete("/api/users/{user_id}")
def delete_user(user_id: str):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return {"message": "User deleted successfully"}

@app.get("/api/ingredients")
def read_ingredients():
    db = SessionLocal()
    ingredients = db.query(Ingredient).all()
    return [ingredient_to_dict(ingredient) for ingredient in ingredients]

@app.post("/api/ingredients")
def create_ingredient(ingredient_data: IngredientInput):
    db = SessionLocal()
    ingredient = Ingredient(
        name=ingredient_data.name,
        unit=ingredient_data.unit
    )
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient_to_dict(ingredient)

@app.put("/api/ingredients/{ingredient_id}")
def update_ingredient(ingredient_id: str, ingredient_data: IngredientInput):
    db = SessionLocal()
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if db_ingredient:
        db_ingredient.name = ingredient_data.name
        db_ingredient.unit = ingredient_data.unit
        db.commit()
        db.refresh(db_ingredient)
    return ingredient_to_dict(db_ingredient)

@app.delete("/api/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: str):
    db = SessionLocal()
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if db_ingredient:
        db.delete(db_ingredient)
        db.commit()
    return {"message": "Ingredient deleted successfully"}

@app.get("/api/cocktail-ingredients")
def read_cocktail_ingredients():
    db = SessionLocal()
    cocktail_ingredients = db.query(CocktailIngredient).all()
    return [cocktail_ingredient_to_dict(ci) for ci in cocktail_ingredients]

@app.post("/api/cocktail-ingredients")
def create_cocktail_ingredient(cocktail_ingredient_data: CocktailIngredientInput):
    db = SessionLocal()
    cocktail_ingredient = CocktailIngredient(
        cocktail_id=cocktail_ingredient_data.cocktail_id,
        ingredient_id=cocktail_ingredient_data.ingredient_id,
        quantity=cocktail_ingredient_data.quantity
    )
    db.add(cocktail_ingredient)
    db.commit()
    db.refresh(cocktail_ingredient)
    return cocktail_ingredient_to_dict(cocktail_ingredient)

@app.put("/api/cocktail-ingredients/{cocktail_ingredient_id}")
def update_cocktail_ingredient(cocktail_ingredient_id: str, cocktail_ingredient_data: CocktailIngredientInput):
    db = SessionLocal()
    db_cocktail_ingredient = db.query(CocktailIngredient).filter(CocktailIngredient.id == cocktail_ingredient_id).first()
    if db_cocktail_ingredient:
        db_cocktail_ingredient.quantity = cocktail_ingredient_data.quantity
        db.commit()
        db.refresh(db_cocktail_ingredient)
    return cocktail_ingredient_to_dict(db_cocktail_ingredient)

@app.delete("/api/cocktail-ingredients/{cocktail_ingredient_id}")
def delete_cocktail_ingredient(cocktail_ingredient_id: str):
    db = SessionLocal()
    db_cocktail_ingredient = db.query(CocktailIngredient).filter(CocktailIngredient.id == cocktail_ingredient_id).first()
    if db_cocktail_ingredient:
        db.delete(db_cocktail_ingredient)
        db.commit()
    return {"message": "Cocktail ingredient deleted successfully"}

@app.get("/api/favorites")
def read_favorites():
    db = SessionLocal()
    favorites = db.query(Favorite).all()
    return [favorite_to_dict(favorite) for favorite in favorites]

@app.post("/api/favorites")
def create_favorite(favorite_data: FavoriteInput):
    db = SessionLocal()
    favorite = Favorite(
        user_id=favorite_data.user_id,
        cocktail_id=favorite_data.cocktail_id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite_to_dict(favorite)

@app.delete("/api/favorites/{favorite_id}")
def delete_favorite(favorite_id: str):
    db = SessionLocal()
    db_favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return {"message": "Favorite deleted successfully"}

@app.get("/api/user-ingredients")
def read_user_ingredients():
    db = SessionLocal()
    user_ingredients = db.query(UserIngredient).all()
    return user_ingredients

@app.post("/api/user-ingredients")
def create_user_ingredient(user_ingredient_data: UserIngredientInput):
    db = SessionLocal()
    user_ingredient = UserIngredient(
        user_id=user_ingredient_data.user_id,
        ingredient_id=user_ingredient_data.ingredient_id
    )
    db.add(user_ingredient)
    db.commit()
    db.refresh(user_ingredient)
    return user_ingredient_to_dict(user_ingredient)

@app.delete("/api/user-ingredients/{user_ingredient_id}")
def delete_user_ingredient(user_ingredient_id: str):
    db = SessionLocal()
    db_user_ingredient = db.query(UserIngredient).filter(UserIngredient.id == user_ingredient_id).first()
    if db_user_ingredient:
        db.delete(db_user_ingredient)
        db.commit()
    return {"message": "User ingredient deleted successfully"}

@app.get("/api/ratings")
def read_ratings():
    db = SessionLocal()
    ratings = db.query(Rating).all()
    return [rating_to_dict(rating) for rating in ratings]

@app.post("/api/ratings")
def create_rating(rating_data: RatingInput):
    db = SessionLocal()
    rating = Rating(
        user_id=rating_data.user_id,
        cocktail_id=rating_data.cocktail_id,
        rating=rating_data.rating
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating_to_dict(rating)

@app.put("/api/ratings/{rating_id}")
def update_rating(rating_id: str, rating_data: RatingInput):
    db = SessionLocal()
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if db_rating:
        db_rating.rating = rating_data.rating
        db.commit()
        db.refresh(db_rating)
    return rating_to_dict(db_rating)

@app.delete("/api/ratings/{rating_id}")
def delete_rating(rating_id: str):
    db = SessionLocal()
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return {"message": "Rating deleted successfully"}

# Routes pour servir les pages HTML
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return f.read()

@app.get("/cocktails", response_class=HTMLResponse)
async def read_cocktails_page():
    with open("static/cocktails.html") as f:
        return f.read()

@app.get("/users", response_class=HTMLResponse)
async def read_users_page():
    with open("static/users.html") as f:
        return f.read()

@app.get("/ingredients", response_class=HTMLResponse)
async def read_ingredients_page():
    with open("static/ingredients.html") as f:
        return f.read()

@app.get("/cocktail-ingredients", response_class=HTMLResponse)
async def read_cocktail_ingredients_page():
    with open("static/cocktail-ingredients.html") as f:
        return f.read()

@app.get("/favorites", response_class=HTMLResponse)
async def read_favorites_page():
    with open("static/favorites.html") as f:
        return f.read()

@app.get("/user-ingredients", response_class=HTMLResponse)
async def read_user_ingredients_page():
    with open("static/user-ingredients.html") as f:
        return f.read()

@app.get("/ratings", response_class=HTMLResponse)
async def read_ratings_page():
    with open("static/ratings.html") as f:
        return f.read()

# Fonction d'initialisation de la base de données
def init_db():
    try:
        # Créer le dossier data s'il n'existe pas
        os.makedirs("./data", exist_ok=True)
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

        # Insérer des données de test si la base est vide
        db = SessionLocal()
        if not db.query(User).first():  # Vérifie si la table users est vide
            # Insérer les données de test ici
            test_user = User(
                id=str(uuid4()),
                email="test@example.com",
                password="password123",
                name="Test User"
            )
            db.add(test_user)
            db.commit()
            print("Test data inserted successfully!")
        db.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialiser la base de données au démarrage
@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    init_db()

# Après la création de l'engine
try:
    connection = engine.connect()
    connection.close()
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {str(e)}")

# Ajoutez ces fonctions de conversion après vos modèles
def cocktail_to_dict(cocktail):
    return {
        "id": cocktail.id,
        "name": cocktail.name,
        "description": cocktail.description,
        "image": cocktail.image,
        "recipe": cocktail.recipe,
        "user_id": cocktail.user_id
    }

def user_to_dict(user):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "password": user.password  # Note: en production, ne jamais renvoyer le mot de passe
    }

def ingredient_to_dict(ingredient):
    return {
        "id": ingredient.id,
        "name": ingredient.name,
        "unit": ingredient.unit
    }

def cocktail_ingredient_to_dict(cocktail_ingredient):
    return {
        "id": cocktail_ingredient.id,
        "cocktail_id": cocktail_ingredient.cocktail_id,
        "ingredient_id": cocktail_ingredient.ingredient_id,
        "quantity": float(cocktail_ingredient.quantity)
    }

def favorite_to_dict(favorite):
    return {
        "id": favorite.id,
        "user_id": favorite.user_id,
        "cocktail_id": favorite.cocktail_id
    }

def rating_to_dict(rating):
    return {
        "id": rating.id,
        "user_id": rating.user_id,
        "cocktail_id": rating.cocktail_id,
        "rating": float(rating.rating)
    }

def user_ingredient_to_dict(user_ingredient):
    return {
        "id": user_ingredient.id,
        "user_id": user_ingredient.user_id,
        "ingredient_id": user_ingredient.ingredient_id
    }