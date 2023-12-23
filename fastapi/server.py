import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
import pandas as pd
from typing import List
from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

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


class ListaCanciones(BaseModel):
    canciones: List[Cancion]


app = FastAPI(
    title="Servidor de datos",
    description="Datos de canciones de Taylor Swift.",
    version="0.1.0",
)



# Modificando la función retrieve_data
@app.post("/retrieve_data/")
async def retrieve_data(file: UploadFile = File(...)):
    try:
        contenido_csv = await file.read()
        df = pd.read_csv(io.BytesIO(contenido_csv), sep=',')
        df = df.fillna(0)
        df_dict = df.to_dict(orient='records')
        listado = ListaCanciones()
        listado.canciones = df_dict
        return listado
    except Exception as e:
        return JSONResponse(content=f"Error: {str(e)}", status_code=500)
