import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

class Cancion(BaseModel):
    x: int
    name: str
    album: str
    track_number: int
    release_date: str
    id: str
    uri: str
    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    liveness: float
    loudness: float
    speechiness: float
    tempo: float
    valence: float
    popularity: int
    duration_ms: int

class ListadoContratos(BaseModel):
    contratos: List[dict]

app = FastAPI(
    title="Servidor de datos",
    description="Datos de canciones de Taylor Swift.",
    version="0.1.0",
)

@app.get("/retrieve_data/")
def retrieve_data():
    try:
        # Lee el archivo CSV
        taylor_swift_data = pd.read_csv('./taylor_swift_spotify.csv', sep=',')
        taylor_swift_data = taylor_swift_data.fillna(0)

        # Convierte los datos a un formato de diccionario
        taylor_swift_data_dict = taylor_swift_data.to_dict(orient='records')

        # Crea una instancia de ListadoContratos y asigna los datos
        listado = ListadoContratos()
        listado.contratos = taylor_swift_data_dict

        return listado
    except Exception as e:
        # Registra el error en los logs y devuelve una respuesta 500
        print(f"Error: {str(e)}")
        return JSONResponse(content=f"Error: {str(e)}", status_code=500)
