from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI()

# Define the path to a writeable directory (for example, /tmp/)
JSON_FILE_PATH = "/tmp/LWINdatabase.json"

# Load wines from the JSON file
def load_wines():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    return []

# Save wines to the JSON file
def save_wines(wines_db):
    with open(JSON_FILE_PATH, "w") as file:
        json.dump(wines_db, file, indent=4)

# Initialize wines_db from JSON file
wines_db = load_wines()

# Define the Wine model
class Wine(BaseModel):
    LWIN: float
    STATUS: str
    DISPLAY_NAME: str
    PRODUCER_TITLE: Optional[str] = None
    PRODUCER_NAME: Optional[str] = None
    WINE: str
    COUNTRY: str
    REGION: Optional[str] = None
    SUB_REGION: Optional[str] = None
    SITE: Optional[str] = None
    PARCEL: Optional[str] = None
    COLOUR: Optional[str] = None
    TYPE: str
    SUB_TYPE: str
    DESIGNATION: Optional[str] = None
    CLASSIFICATION: Optional[str] = None
    VINTAGE_CONFIG: Optional[str] = None
    FIRST_VINTAGE: Optional[float] = None
    FINAL_VINTAGE: Optional[float] = None
    DATE_ADDED: str
    DATE_UPDATED: str
    REFERENCE: Optional[str] = None
    is_favourite: Optional[bool] = False
    is_disliked: Optional[bool] = False

# Add root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Wine API"}

# Endpoint to add a wine
@app.post("/wines/")
def add_wine(wine: Wine):
    for existing_wine in wines_db:
        if existing_wine['LWIN'] == wine.LWIN:
            raise HTTPException(status_code=400, detail="Wine already exists")
    wines_db.append(wine.dict())
    save_wines(wines_db)
    return {"message": "Wine added successfully", "wine": wine}

# Endpoint to query wines by fields
@app.get('/wines/')
def query_wines(LWIN: Optional[float] = None, COUNTRY: Optional[str] = None, WINE: Optional[str] = None):
    results = []
    for wine in wines_db:
        if (LWIN is None or wine['LWIN'] == LWIN) and \
           (COUNTRY is None or wine['COUNTRY'].lower() == COUNTRY.lower()) and \
           (WINE is None or wine['WINE'].lower() == WINE.lower()):
            results.append(wine)
    if not results:
        raise HTTPException(status_code=404, detail="No wines found.")
    return results

# Endpoint to remove a wine
@app.delete("/wines/{lwin}")
def remove_wine(lwin: float):
    global wines_db
    wines_db = [wine for wine in wines_db if wine['LWIN'] != lwin]
    save_wines(wines_db)
    return {"message": f"Wine with LWIN {lwin} removed"}

# Endpoint to mark a wine as favourite
@app.patch("/wines/{lwin}/favourite")
def mark_favourite_wine(lwin: float):
    for wine in wines_db:
        if wine['LWIN'] == lwin:
            wine['is_favourite'] = True
            save_wines(wines_db)
            return {"message": f"Wine with LWIN {lwin} marked as favourite"}
    raise HTTPException(status_code=404, detail="Wine not found.")

# Endpoint to mark a wine as disliked
@app.patch("/wines/{lwin}/dislike")
def mark_disliked_wine(lwin: float):
    for wine in wines_db:
        if wine['LWIN'] == lwin:
            wine['is_disliked'] = True
            save_wines(wines_db)
            return {"message": f"Wine with LWIN {lwin} marked as disliked"}
    raise HTTPException(status_code=404, detail="Wine not found.")

# Endpoint to list all wines
@app.get("/wines/all")
def list_all_wines():
    return wines_db
