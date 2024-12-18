from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse  # Add this line
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, Numeric, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import Optional
import uuid

DATABASE_URL = "postgresql://user:password@db/cocktail_db"  
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Cocktail_ingredient(Base):
    __tablename__ = "cocktail_ingredients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cocktail_id = Column(UUID(as_uuid=True), ForeignKey("cocktails.id"))
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))
    quantity = Column(Numeric)
    
class Cocktail(Base):
    __tablename__ = "cocktails"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    image = Column(String)
    recipe = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

class Favorites(Base):
    __tablename__ = "favorites"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    cocktail_id = Column(UUID(as_uuid=True), ForeignKey("cocktails.id"))

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    unit = Column(String)
    
class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    cocktail_id = Column(UUID(as_uuid=True), ForeignKey("cocktails.id"))
    rating = Column(Numeric)
    
class User_ingredient(Base):
    __tablename__ = "user_ingredients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))
    
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)

class CocktailCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    recipe: Optional[str] = None
    user_id: uuid.UUID

class CocktailResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    image: Optional[str]
    recipe: Optional[str]

class IngredientCreate(BaseModel):
    name: str
    unit: Optional[str] = None

class IngredientResponse(BaseModel):
    id: uuid.UUID
    name: str
    unit: Optional[str]

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: Optional[str]

class RatingsCreate(BaseModel):
    user_id: uuid.UUID
    cocktail_id: uuid.UUID
    rating: float

class RatingsResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    cocktail_id: uuid.UUID
    rating: float

class FavoritesCreate(BaseModel):
    user_id: uuid.UUID
    cocktail_id: uuid.UUID

class FavoritesResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    cocktail_id: uuid.UUID

class UserIngredientCreate(BaseModel):
    user_id: uuid.UUID
    ingredient_id: uuid.UUID

class UserIngredientResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ingredient_id: uuid.UUID

class CocktailIngredientCreate(BaseModel):
    cocktail_id: uuid.UUID
    ingredient_id: uuid.UUID
    quantity: float

class CocktailIngredientResponse(BaseModel):
    id: uuid.UUID
    cocktail_id: uuid.UUID
    ingredient_id: uuid.UUID
    quantity: float

# Initialisation de l'application
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route for the home page
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'application Cocktail Odyssey!"}

# Route for the HTML home page
@app.get("/home")
def home():
    return FileResponse("static/index.html")

# Routes pour les cocktails
@app.get("/cocktails", response_model=list[CocktailResponse])
def get_cocktails(db: SessionLocal = Depends(get_db)):
    return db.query(Cocktail).all()

@app.post("/cocktails", response_model=CocktailResponse)
def create_cocktail(cocktail: CocktailCreate, db: SessionLocal = Depends(get_db)):
    new_cocktail = Cocktail(**cocktail.dict())
    db.add(new_cocktail)
    db.commit()
    db.refresh(new_cocktail)
    return new_cocktail

@app.put("/cocktails/{cocktail_id}", response_model=CocktailResponse)
def update_cocktail(cocktail_id: uuid.UUID, cocktail: CocktailCreate, db: SessionLocal = Depends(get_db)):
    cocktail_record = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if not cocktail_record:
        raise HTTPException(status_code=404, detail="Cocktail non trouvé")
    update_data = cocktail.dict()
    for key, value in update_data.items():
        setattr(cocktail_record, key, value)
    db.commit()
    db.refresh(cocktail_record)
    return cocktail_record

@app.delete("/cocktails/{cocktail_id}", status_code=204)
def delete_cocktail(cocktail_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    cocktail = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail non trouvé")
    db.delete(cocktail)
    db.commit()
    return {"message": "Cocktail supprimé avec succès"}

# Routes pour les ingrédients
@app.get("/ingredients", response_model=list[IngredientResponse])
def get_ingredients(db: SessionLocal = Depends(get_db)):
    return db.query(Ingredient).all()

@app.post("/ingredients", response_model=IngredientResponse)
def create_ingredient(ingredient: IngredientCreate, db: SessionLocal = Depends(get_db)):
    new_ingredient = Ingredient(**ingredient.dict())
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

@app.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: uuid.UUID, ingredient: IngredientCreate, db: SessionLocal = Depends(get_db)):
    ingredient_record = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient_record:
        raise HTTPException(status_code=404, detail="Ingrédient non trouvé")
    update_data = ingredient.dict()
    for key, value in update_data.items():
        setattr(ingredient_record, key, value)
    db.commit()
    db.refresh(ingredient_record)
    return ingredient_record

@app.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrédient non trouvé")
    db.delete(ingredient)
    db.commit()
    return {"message": "Ingrédient supprimé avec succès"}

# Routes pour les utilisateurs
@app.get("/users", response_model=list[UserResponse])
def get_users(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: uuid.UUID, user: UserCreate, db: SessionLocal = Depends(get_db)):
    user_record = db.query(User).filter(User.id == user_id).first()
    if not user_record:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    update_data = user.dict()
    for key, value in update_data.items():
        setattr(user_record, key, value)
    db.commit()
    db.refresh(user_record)
    return user_record

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}

# Routes pour les évaluations
@app.get("/ratings", response_model=list[RatingsResponse])
def get_ratings(db: SessionLocal = Depends(get_db)):
    return db.query(Ratings).all()

@app.post("/ratings", response_model=RatingsResponse)
def create_rating(rating: RatingsCreate, db: SessionLocal = Depends(get_db)):
    new_rating = Ratings(**rating.dict())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@app.put("/ratings/{rating_id}", response_model=RatingsResponse)
def update_rating(rating_id: uuid.UUID, rating: RatingsCreate, db: SessionLocal = Depends(get_db)):
    rating_record = db.query(Ratings).filter(Ratings.id == rating_id).first()
    if not rating_record:
        raise HTTPException(status_code=404, detail="Évaluation non trouvée")
    update_data = rating.dict()
    for key, value in update_data.items():
        setattr(rating_record, key, value)
    db.commit()
    db.refresh(rating_record)
    return rating_record

@app.delete("/ratings/{rating_id}", status_code=204)
def delete_rating(rating_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    rating = db.query(Ratings).filter(Ratings.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Évaluation non trouvée")
    db.delete(rating)
    db.commit()
    return {"message": "Évaluation supprimée avec succès"}

# Routes pour les favoris
@app.get("/favorites", response_model=list[FavoritesResponse])
def get_favorites(db: SessionLocal = Depends(get_db)):
    return db.query(Favorites).all()

@app.put("/favorites/{favorite_id}", response_model=FavoritesResponse)
def update_favorite(favorite_id: uuid.UUID, favorite: FavoritesCreate, db: SessionLocal = Depends(get_db)):
    favorite_record = db.query(Favorites).filter(Favorites.id == favorite_id).first()
    if not favorite_record:
        raise HTTPException(status_code=404, detail="Favori non trouvé")
    update_data = favorite.dict()
    for key, value in update_data.items():
        setattr(favorite_record, key, value)
    db.commit()
    db.refresh(favorite_record)
    return favorite_record

@app.post("/favorites", response_model=FavoritesResponse)
def create_favorite(favorite: FavoritesCreate, db: SessionLocal = Depends(get_db)):
    new_favorite = Favorites(**favorite.dict())
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    return new_favorite

@app.delete("/favorites/{favorite_id}", status_code=204)
def delete_favorite(favorite_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    favorite = db.query(Favorites).filter(Favorites.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favori non trouvé")
    db.delete(favorite)
    db.commit()
    return {"message": "Favori supprimé avec succès"}

# Routes pour les ingrédients de l'utilisateur
@app.get("/user_ingredients", response_model=list[UserIngredientResponse])
def get_user_ingredients(db: SessionLocal = Depends(get_db)):
    return db.query(User_ingredient).all()

@app.put("/user_ingredients/{user_ingredient_id}", response_model=UserIngredientResponse)
def update_user_ingredient(user_ingredient_id: uuid.UUID, user_ingredient: UserIngredientCreate, db: SessionLocal = Depends(get_db)):
    user_ingredient_record = db.query(User_ingredient).filter(User_ingredient.id == user_ingredient_id).first()
    if not user_ingredient_record:
        raise HTTPException(status_code=404, detail="Ingrédient de l'utilisateur non trouvé")
    update_data = user_ingredient.dict()
    for key, value in update_data.items():
        setattr(user_ingredient_record, key, value)
    db.commit()
    db.refresh(user_ingredient_record)
    return user_ingredient_record


@app.post("/user_ingredients", response_model=UserIngredientResponse)
def create_user_ingredient(user_ingredient: UserIngredientCreate, db: SessionLocal = Depends(get_db)):
    new_user_ingredient = User_ingredient(**user_ingredient.dict())
    db.add(new_user_ingredient)
    db.commit()
    db.refresh(new_user_ingredient)
    return new_user_ingredient

@app.delete("/user_ingredients/{user_ingredient_id}", status_code=204)
def delete_user_ingredient(user_ingredient_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    user_ingredient = db.query(User_ingredient).filter(User_ingredient.id == user_ingredient_id).first()
    if not user_ingredient:
        raise HTTPException(status_code=404, detail="Ingrédient de l'utilisateur non trouvé")
    db.delete(user_ingredient)
    db.commit()
    return {"message": "Ingrédient de l'utilisateur supprimé avec succès"}

# Routes pour les ingrédients du cocktail
@app.get("/cocktail_ingredients", response_model=list[CocktailIngredientResponse])
def get_cocktail_ingredients(db: SessionLocal = Depends(get_db)):
    return db.query(Cocktail_ingredient).all()

@app.post("/cocktail_ingredients", response_model=CocktailIngredientResponse)
def create_cocktail_ingredient(cocktail_ingredient: CocktailIngredientCreate, db: SessionLocal = Depends(get_db)):
    new_cocktail_ingredient = Cocktail_ingredient(**cocktail_ingredient.dict())
    db.add(new_cocktail_ingredient)
    db.commit()
    db.refresh(new_cocktail_ingredient)
    return new_cocktail_ingredient

@app.put("/cocktail_ingredients/{cocktail_ingredient_id}", response_model=CocktailIngredientResponse)
def update_cocktail_ingredient(cocktail_ingredient_id: uuid.UUID, cocktail_ingredient: CocktailIngredientCreate, db: SessionLocal = Depends(get_db)):
    cocktail_ingredient_record = db.query(Cocktail_ingredient).filter(Cocktail_ingredient.id == cocktail_ingredient_id).first()
    if not cocktail_ingredient_record:
        raise HTTPException(status_code=404, detail="Ingrédient du cocktail non trouvé")
    update_data = cocktail_ingredient.dict()
    for key, value in update_data.items():
        setattr(cocktail_ingredient_record, key, value)
    db.commit()
    db.refresh(cocktail_ingredient_record)
    return cocktail_ingredient_record

@app.delete("/cocktail_ingredients/{cocktail_ingredient_id}", status_code=204)
def delete_cocktail_ingredient(cocktail_ingredient_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    cocktail_ingredient = db.query(Cocktail_ingredient).filter(Cocktail_ingredient.id == cocktail_ingredient_id).first()
    if not cocktail_ingredient:
        raise HTTPException(status_code=404, detail="Ingrédient du cocktail non trouvé")
    db.delete(cocktail_ingredient)
    db.commit()
    return {"message": "Ingrédient du cocktail supprimé avec succès"}

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(bind=engine)  # Assure la création des tables
    uvicorn.run(app, host="127.0.0.1", port=8000)


