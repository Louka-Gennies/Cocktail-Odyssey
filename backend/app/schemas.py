from pydantic import BaseModel
from typing import Optional

class CocktailBase(BaseModel):
    name: str
    description: str
    ingredients: str
    instructions: str

class CocktailCreate(CocktailBase):
    pass

class Cocktail(CocktailBase):
    id: int

    class Config:
        orm_mode = True