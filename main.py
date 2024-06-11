from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from typing import List, Optional
from pydantic import BaseModel, Field

app=FastAPI(
    title="FastApi CRUD",
    description='An example of how to use FastApi',
    version="0.0.1",
)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview:str
    year: int
    rating: float
    category: str
    
movies=[]
    
@app.get("/api", tags=['Start Root'])
def readRoot():
    return HTMLResponse("<h1>FastApi</h1>")

@app.get('/movies', tags=['Get Movies'])
def getMovies():
    return movies

@app.get('/movies/{id}', tags=['Get Movies By Id'])
def getMovieById(id: int):
    if id is None or id <= 0: 
        raise HTTPException(status_code=400, detail='Id no valido')
    try:
        for movie in movies:
            if movie.id == id:
                return movie
        else:  
            raise HTTPException(status_code=404, detail=f'Pelicula con el id: {id} no encontrada')
    except Exception as e: 
        raise HTTPException(status_code=500, detail='Error al procesar tu solicitud')
    

@app.get('/movies/category/{category}', tags=['Get Movies By Category'])
async def getMoviesByCategory(category: str):
    if category is None or category == '':
        raise HTTPException(status_code=400, detail="Categoria no valida")
    try:
        foundMovies = [movie for movie in movies if movie.category.lower() == category.lower()]
        if not foundMovies:
            raise HTTPException(status_code=404, detail=f"No hay peliculas encontradas con la categoria:'{category}'.")
        return foundMovies
    except Exception as e: 
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.post('/movies', tags=['Create A Movie'])
def createMovie(movie: Movie):
    try:
        if any(item['id'] == id for item in movies):
            raise HTTPException(status_code=400, detail=f"Pelicula con el id: {id} ya existe")
        
        movies.append(movie)
        return "Pelicula creada correctamente"
    
    except Exception as e: 
        raise HTTPException(status_code=500, detail="Ha ocurrido un error al procesar tu solicitud")

    
@app.put("/movies/update/{id}", tags=["Update Movie By Id"])
def updateMovieById(id: int, updatedMovie: Movie):
    for i, movie in enumerate(movies):
        if movie.id == id:
            movies[i] = updatedMovie
            return {"message": "Pelicula actualizada correctamente"}
    raise HTTPException(status_code=404, detail=f"Pelicula con el id: {id} no encontrada")
                        
@app.delete('/movies/delete/{id}', tags=['Delete Movie By Id'])
def deleteMovieById(id: int):
    if id is None or id <= 0: 
        raise HTTPException(status_code=400, detail="Id no valido")
    try:
        for i, movie in enumerate(movies):
            if movie.id == id:
                del movies[i]
                return {"message": "Pelicula eliminada correctamente"}
        else: 
            raise HTTPException(status_code=404, detail=f"Pelicula con el id: {id} no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ha ocurrido un error al procesar tu solicitud")