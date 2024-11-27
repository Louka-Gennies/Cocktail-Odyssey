from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
import uuid

# Configuration de la base
DATABASE_URL = "sqlite:///./cocktail.db"  # Remplacez par l'URL de votre base si autre
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour les sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèles SQLAlchemy
class Cocktail(Base):
    __tablename__ = "cocktails"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    image = Column(String)
    recipe = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)

# Modèles Pydantic pour validation
class CocktailCreate(BaseModel):
    name: str
    description: str | None = None
    image: str | None = None
    recipe: str | None = None

class CocktailResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    image: str | None
    recipe: str | None

    class Config:
        orm_mode = True

# Initialisation de l'application
app = FastAPI()

# Route pour récupérer tous les cocktails
@app.get("/cocktails", response_model=list[CocktailResponse])
def get_cocktails(db: SessionLocal = Depends(get_db)):
    return db.query(Cocktail).all()

# Route pour ajouter un cocktail
@app.post("/cocktails", response_model=CocktailResponse)
def create_cocktail(cocktail: CocktailCreate, db: SessionLocal = Depends(get_db)):
    new_cocktail = Cocktail(**cocktail.dict())
    db.add(new_cocktail)
    db.commit()
    db.refresh(new_cocktail)
    return new_cocktail

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(bind=engine)  # Assure la création des tables
    uvicorn.run(app, host="127.0.0.1", port=8000)
