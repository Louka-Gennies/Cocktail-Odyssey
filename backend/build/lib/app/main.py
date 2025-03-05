from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# Créer les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cocktails/", response_model=schemas.Cocktail)
def create_cocktail(cocktail: schemas.CocktailCreate, db: Session = Depends(get_db)):
    return crud.create_cocktail(db=db, cocktail=cocktail)

@app.get("/cocktails/", response_model=list[schemas.Cocktail])
def read_cocktails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cocktails = crud.get_cocktails(db, skip=skip, limit=limit)
    return cocktails

@app.get("/cocktails/{cocktail_id}", response_model=schemas.Cocktail)
def read_cocktail(cocktail_id: int, db: Session = Depends(get_db)):
    db_cocktail = crud.get_cocktail(db, cocktail_id=cocktail_id)
    if db_cocktail is None:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    return db_cocktail