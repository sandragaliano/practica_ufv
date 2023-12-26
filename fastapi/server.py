import shutil
import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form
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

class ListadoCanciones(BaseModel):
    canciones = List[Cancion]

app = FastAPI(
    title="Servidor de datos",
    description="Datos de canciones de Taylor Swift.",
    version="0.1.0",
)

@app.get("/retrieve_data/")
def retrieve_data():
    todosmisdatos = pd.read_csv('./taylor_swift_spotify.csv',sep=',')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = ListadoCanciones()
    listado.canciones = todosmisdatosdict
    return listado