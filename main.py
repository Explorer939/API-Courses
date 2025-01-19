from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import pandas as pd
import uvicorn
import threading
import time

# Création de l'application FastAPI
app = FastAPI()
# Chargement du fichier CSV

csv_file_path = "courses.csv"
data_lock = threading.Lock()
courses_df = pd.read_csv(csv_file_path)

def load_data():
    global df
    while True:
        with data_lock:
            df = pd.read_csv(csv_file_path)
        time.sleep(60)  # Mise à jour toutes les minutes

# Démarrage de la mise à jour automatique
threading.Thread(target=load_data, daemon=True).start()

# Nettoyage des colonnes
with data_lock:
    df.columns = df.columns.str.strip().str.lower()

# Convertir les données en liste de dictionnaires
courses_data = courses_df.to_dict(orient="records")

# Page d'accueil
@app.get("/")
def read_root():
    return {"message": "Free online course API with filters on course type and difficulty."}

# Endpoint pour récupérer tous les cours
@app.get("/courses")

def get_courses(
    skip: int = 0, 
    limit: int = 100, 
    sort_by: Optional[str] = Query(None, enum=["Enrolled Student Count", "Course Rating"], description="Sort by number of students or course rate"),
    sort_order: Optional[str] = Query("desc", enum=["asc", "desc"], description="Ascending or descending order")
):
    with data_lock:
        courses = df.copy()

    if sort_by:
        ascending = sort_order == "asc"
        courses[sort_by] = pd.to_numeric(courses[sort_by], errors='coerce')
        courses = courses.sort_values(by=sort_by, ascending=ascending)

    paginated_courses = courses.iloc[skip: skip + limit]
    return paginated_courses.to_dict(orient="records")

# Endpoint pour filtrer par type de produit d'apprentissage
@app.get("/courses/product_type/{product_type}")
def get_courses_by_product_type(product_type: str):
    with data_lock:
        filtered_courses = df[df["Learning Product Type"].str.upper() == product_type.upper()]
    if filtered_courses.empty:
        raise HTTPException(status_code=404, detail="Invalid course type chosen")
    return filtered_courses.to_dict(orient="records")

# Endpoint pour filtrer par niveau de difficulté
@app.get("/courses/difficulty/{difficulty}")
def get_courses_by_difficulty(difficulty: str):
    with data_lock:
        filtered_courses = df[df["Course Difficulty"].str.upper() == difficulty.upper()]
    if filtered_courses.empty:
        raise HTTPException(status_code=404, detail="No course found for this difficulty level")
    return filtered_courses.to_dict(orient="records")

# Endpoint pour combiner les filtres : type de produit + difficulté
@app.get("/courses/filter/")
def filter_courses(
    product_type: Optional[str] = None, 
    difficulty: Optional[str] = None,
    skip: int = 0, 
    limit: int = 10
):
    with data_lock:
        filtered_courses = df.copy()

    if product_type:
        filtered_courses = filtered_courses[filtered_courses["Learning Product Type"].str.upper() == product_type.upper()]
    if difficulty:
        filtered_courses = filtered_courses[filtered_courses["Course Rating"].str.upper() == difficulty.upper()]
    
    paginated_courses = filtered_courses.iloc[skip: skip + limit]
    if paginated_courses.empty:
        raise HTTPException(status_code=404, detail="No courses found with the specified criteria")
    return paginated_courses.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
