from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Create app
app = FastAPI(
    title="Inventory API",
    description="A simple example FastAPI app",
    version="1.0.0"
)

# Data model
class Item(BaseModel):
    id: int
    name: str = Field(..., example="Laptop")
    quantity: int = Field(..., ge=0, example=10)
    description: Optional[str] = None

# Fake in-memory DB
items_db: List[Item] = []

# Routes
@app.get("/service1")
def service1():
    return {"message": "This is the endpoint for service1"}

# you can hardcode the response
@app.get("/service2")
def service2():
    return {
        "name": "service2",
        "foo": "bar",
        "zoo": "baz"
    }

# post a new item
@app.post("/service2/items", response_model=Item)
def create_item(item: Item):
    # Prevent duplicates
    for existing in items_db:
        if existing.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item

# get all items
@app.get("/service2/items", response_model=List[Item])
def get_items():
    return items_db

# get a specific item
@app.get("/service2/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# update an item
@app.put("/service2/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for i, existing in enumerate(items_db):
        if existing.id == item_id:
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# delete an item by id
@app.delete("/service2/items/{item_id}")
def delete_item(item_id: int):
    for i, existing in enumerate(items_db):
        if existing.id == item_id:
            items_db.pop(i)
            return {"status": "success", "message": f"Item {item_id} deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# you can add as much as endpoint by following the above patterns
# run the server with uvicorn main:app --reload --host 0.0.0.0 --port 8000
