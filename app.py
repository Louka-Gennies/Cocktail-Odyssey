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

# Routes pour récupérer les données
@app.get("/api/cocktails")
def read_cocktails():
    db = SessionLocal()
    cocktails = db.query(Cocktail).all()
    return cocktails

@app.get("/api/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    return users

@app.get("/api/ingredients")
def read_ingredients():
    db = SessionLocal()
    ingredients = db.query(Ingredient).all()
    return ingredients

@app.get("/api/cocktail-ingredients")
def read_cocktail_ingredients():
    db = SessionLocal()
    cocktail_ingredients = db.query(CocktailIngredient).all()
    return cocktail_ingredients

@app.get("/api/favorites")
def read_favorites():
    db = SessionLocal()
    favorites = db.query(Favorite).all()
    return favorites

@app.get("/api/user-ingredients")
def read_user_ingredients():
    db = SessionLocal()
    user_ingredients = db.query(UserIngredient).all()
    return user_ingredients

@app.get("/api/ratings")
def read_ratings():
    db = SessionLocal()
    ratings = db.query(Rating).all()
    return ratings

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