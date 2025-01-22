from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, Numeric, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional, List
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

# Route pour la page d'accueil
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'application Cocktail Odyssey!"}

# Route pour la page HTML d'accueil
@app.get("/home")
def home():
    return FileResponse("static/index.html")

# Route pour créer un utilisateur
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Route pour obtenir la liste des utilisateurs
@app.get("/users", response_model=List[UserResponse])
def get_users(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()

# Route pour créer un cocktail
@app.post("/cocktails", response_model=CocktailResponse)
def create_cocktail(cocktail: CocktailCreate, db: SessionLocal = Depends(get_db)):
    new_cocktail = Cocktail(**cocktail.dict())
    db.add(new_cocktail)
    db.commit()
    db.refresh(new_cocktail)
    return new_cocktail

# Route pour obtenir la liste des cocktails
@app.get("/cocktails", response_model=List[CocktailResponse])
def get_cocktails(db: SessionLocal = Depends(get_db)):
    return db.query(Cocktail).all()

# Route pour obtenir les détails d'un cocktail
@app.get("/cocktails/{cocktail_id}", response_model=CocktailResponse)
def get_cocktail(cocktail_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    cocktail = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail non trouvé")
    return cocktail

# Route pour supprimer un cocktail
@app.delete("/cocktails/{cocktail_id}", status_code=204)
def delete_cocktail(cocktail_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    cocktail = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail non trouvé")
    db.delete(cocktail)
    db.commit()
    return {"message": "Cocktail supprimé avec succès"}

# Route pour supprimer un utilisateur
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: uuid.UUID, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(bind=engine)  # Assure la création des tables
    uvicorn.run(app, host="127.0.0.1", port=8000)