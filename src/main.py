from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items")
async def read_items(
    skip: int = 0, limit: int = 15, db: Session = Depends(get_db)
) -> list[schemas.Item]:
    """
    List all items
    """
    items = db.execute(select(models.Item)).scalars().all()
    return items


@app.post("/items")
async def create_item(
    data: schemas.ItemCreate, db: Session = Depends(get_db)
) -> schemas.Item:
    """
    Create new Item
    """
    item = models.Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)) -> schemas.Item:
    item = db.get(models.Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, data: schemas.ItemUpdate, db: Session = Depends(get_db)
) -> schemas.Item:
    """
    Update item
    """
    item = db.get(models.Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, val in data.model_dump(exclude_none=True).items():
        setattr(item, key, val)

    db.commit()
    db.refresh(item)

    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete item
    """
    item = db.get(models.Item, item_id)
    db.delete(item)
    db.commit()
    return {"message": "Item successfully deleted"}
