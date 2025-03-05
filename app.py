# app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from uuid import uuid4

DATABASE_URL = "postgresql://admin:Ynov2025@db/cocktail_db"

engine = create_engine(DATABASE_URL)
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

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes pour récupérer, créer, modifier et supprimer les données

@app.get("/api/cocktails")
def read_cocktails():
    db = SessionLocal()
    cocktails = db.query(Cocktail).all()
    return cocktails

@app.post("/api/cocktails")
def create_cocktail(cocktail: Cocktail):
    db = SessionLocal()
    db.add(cocktail)
    db.commit()
    db.refresh(cocktail)
    return cocktail

@app.put("/api/cocktails/{cocktail_id}")
def update_cocktail(cocktail_id: str, cocktail: Cocktail):
    db = SessionLocal()
    db_cocktail = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if db_cocktail:
        db_cocktail.name = cocktail.name
        db_cocktail.description = cocktail.description
        db_cocktail.image = cocktail.image
        db_cocktail.recipe = cocktail.recipe
        db.commit()
        db.refresh(db_cocktail)
    return db_cocktail

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
    return users

@app.post("/api/users")
def create_user(user: User):
    db = SessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/api/users/{user_id}")
def update_user(user_id: str, user: User):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.email = user.email
        db_user.password = user.password
        db_user.name = user.name
        db.commit()
        db.refresh(db_user)
    return db_user

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
    return ingredients

@app.post("/api/ingredients")
def create_ingredient(ingredient: Ingredient):
    db = SessionLocal()
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

@app.put("/api/ingredients/{ingredient_id}")
def update_ingredient(ingredient_id: str, ingredient: Ingredient):
    db = SessionLocal()
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if db_ingredient:
        db_ingredient.name = ingredient.name
        db_ingredient.unit = ingredient.unit
        db.commit()
        db.refresh(db_ingredient)
    return db_ingredient

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
    return cocktail_ingredients

@app.post("/api/cocktail-ingredients")
def create_cocktail_ingredient(cocktail_ingredient: CocktailIngredient):
    db = SessionLocal()
    db.add(cocktail_ingredient)
    db.commit()
    db.refresh(cocktail_ingredient)
    return cocktail_ingredient

@app.put("/api/cocktail-ingredients/{cocktail_ingredient_id}")
def update_cocktail_ingredient(cocktail_ingredient_id: str, cocktail_ingredient: CocktailIngredient):
    db = SessionLocal()
    db_cocktail_ingredient = db.query(CocktailIngredient).filter(CocktailIngredient.id == cocktail_ingredient_id).first()
    if db_cocktail_ingredient:
        db_cocktail_ingredient.quantity = cocktail_ingredient.quantity
        db.commit()
        db.refresh(db_cocktail_ingredient)
    return db_cocktail_ingredient

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
    return favorites

@app.post("/api/favorites")
def create_favorite(favorite: Favorite):
    db = SessionLocal()
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

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
def create_user_ingredient(user_ingredient: UserIngredient):
    db = SessionLocal()
    db.add(user_ingredient)
    db.commit()
    db.refresh(user_ingredient)
    return user_ingredient

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
    return ratings

@app.post("/api/ratings")
def create_rating(rating: Rating):
    db = SessionLocal()
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

@app.put("/api/ratings/{rating_id}")
def update_rating(rating_id: str, rating: Rating):
    db = SessionLocal()
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if db_rating:
        db_rating.rating = rating.rating
        db.commit()
        db.refresh(db_rating)
    return db_rating

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

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)