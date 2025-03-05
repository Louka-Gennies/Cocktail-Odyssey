from sqlalchemy.orm import Session
from . import models, schemas


def get_cocktail(db: Session, cocktail_id: int):
    return db.query(models.Cocktail).filter(models.Cocktail.id == cocktail_id).first()

def get_cocktails(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cocktail).offset(skip).limit(limit).all()

def create_cocktail(db: Session, cocktail: schemas.CocktailCreate):
    db_cocktail = models.Cocktail(**cocktail.dict())
    db.add(db_cocktail)
    db.commit()
    db.refresh(db_cocktail)
    return db_cocktail