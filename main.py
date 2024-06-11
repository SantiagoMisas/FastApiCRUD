from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from typing import List

app=FastAPI(
    title="FastApi CRUD",
    description='An example of how to use FastApi',
    version="0.0.1",
)

movies = [
    {
        'id': 1,
        'title': 'El padrino',
        'overview': 'El padrino es una pelicula de 1972 dirigida por Francis Ford Coppola',
        'year': 1972,
        'rating': 8.7,
        'category': 'Action'
    }
]

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
            if movie['id'] == id:
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
        foundMovies = [movie for movie in movies if movie['category'].lower() == category.lower()]
        if not foundMovies:
            raise HTTPException(status_code=404, detail=f"No hay peliculas encontradas con la categoria:'{category}'.")
        return foundMovies
    except Exception as e: 
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.post('/movies', tags=['Create A Movie'])
def createMovie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
    ):
    try:
        if any(movie['id'] == id for movie in movies):
            raise HTTPException(status_code=400, detail=f"Pelicula con el id: {id} ya existe")
        
        movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
        })
        return "Pelicula creada correctamente"
    except Exception as e: 
        raise HTTPException(status_code=500, detail="Ha ocurrido un error al procesar tu solicitud")


@app.put('/movies/update/{id}', tags=['Update Movie By Id'])
def updateMovieById(
    id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
                    ):
    if id is None or id <= 0: 
        raise HTTPException(status_code=400, detail="Id no valido")
    try:
        for movie in movies:
            if movie['id'] == id:
                movie['title'] = title
                movie['overview'] = overview
                movie['year'] = year
                movie['rating'] = rating
                movie['category'] = category
                return "Pelicula actualizada correctamente"
        else: 
            raise HTTPException(status_code=404, detail=f"Pelicula con el id: {id} no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ha ocurrido un error al procesar tu solicitud")
    

@app.delete('/movies/delete/{id}', tags=['Delete Movie By Id'])
def deleteMovieById(id: int):
    if id is None or id <= 0: 
        raise HTTPException(status_code=400, detail="Id no valido")
    try:
        for movie in movies:
            if movie['id'] == id:
                movies.remove(movie)
                return "Pelicula eliminada correctamente"
        else: 
            raise HTTPException(status_code=404, detail=f"Pelicula con el id: {id} no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ha ocurrido un error al procesar tu solicitud")