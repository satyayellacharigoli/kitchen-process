from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, Item, get_db
from datetime import datetime
from sqlalchemy import func


app = FastAPI()


class CreateItem(BaseModel):
    name: str
    quantity: int


@app.post("/items/")
def add_item(item: CreateItem, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.name == item.name).first()
    if db_item:
        db_item.quantity += item.quantity
        db_item.updated_at = func.now()
    else:
        db_item = Item(name=item.name, quantity=item.quantity)
        db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/burgers/available/")
def get_available_burgers(db: Session = Depends(get_db)):
    recipe = {"bun": 1, "beef patty": 1, "lettuce": 1, "tomato": 1, "ketchup": 1}
    items = db.query(Item).filter(Item.name.in_(recipe.keys())).all()
    counts = {item.name: item.quantity // recipe[item.name] for item in items}
    return {"burgers_available": min(counts.values()) if counts else 0}
