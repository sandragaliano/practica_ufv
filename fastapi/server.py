import shutil
import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import pandas as pd
from typing import List
from pydantic import BaseModel as PydanticBaseModel
from fastapi.middleware.cors import CORSMiddleware
import streamlit as st


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
    description="""Servimos datos de canciones de Taylor Swift.""",
    version="0.1.0",
)

# Configurar CORS
origins = ["*"]  # Esto permite solicitudes desde cualquier origen, ajusta según sea necesario
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/retrieve_data/")
def retrieve_data():
    try:
        df = pd.read_csv('/home/sandra/repositorios/repos/practica_ufv/streamlit/pages/taylor_swift_spotify.csv')
        # Renombrar columnas según corresponda
        df = df.rename(columns={
            "x": "x",
            "name": "name",
            # ... otras columnas ...
        })
        canciones_dict = df.to_dict(orient='records')
        lista_canciones = ListaCanciones(canciones=canciones_dict)
        return lista_canciones
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Indica a Streamlit que sirva el contenido en la ruta /dashboard
if st.get_option("server.enableCORS"):
    st.markdown(f'<iframe src="http://localhost:8501/" width=1000 height=800></iframe>', unsafe_allow_html=True)
