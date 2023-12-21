import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns

@st.cache_data
def load_data():
    # Cargar conjunto de datos de Taylor Swift
    df = pd.read_csv("taylor_swift_spotify.csv")
    return df

def info_box(texto, color=None):
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{texto}</p></div>', unsafe_allow_html=True)

df = load_data()
registros = str(df.shape[0])

# Gráfica 1: Canciones por álbum:
canciones_por_album = df['album'].value_counts().to_frame().reset_index()
# Cols para la gráfica:
canciones_por_album.columns = ['Album', 'Número de Canciones']
# Pie chart:
canciones_por_album_chart = px.pie(canciones_por_album, names='Album', values='Número de Canciones', title='Número de Canciones por Album')

# Gráfica 2:
# Usamos las 10 canciones con mayor número de popularidad:
canciones_populares = df.nlargest(10, 'popularity')[['name', 'popularity']]
# Gráfico de barras de las 10 con mayor popularidad:
canciones_populares_chart = px.bar(canciones_populares, x='name', y='popularity', title='Top 10 Canciones más Populares', labels={'name': 'Canción', 'popularity': 'Popularidad'})

# Gráfica 3:
# Relación popularidad - danceability (son las canciones más bailables las más populares??)
relacion_popularidad_danceability_chart = px.scatter(df, x='popularity', y='danceability', title='Relación entre Popularidad y Danceability', labels={'popularity': 'Popularidad', 'danceability': 'Danceability'})

sns.set_palette("pastel")

st.header("Información general")

col1, col2, col3 = st.columns(3)

col4, col5, col6 = st.columns(3)
with col1:
    col1.subheader('# canciones')
    info_box(registros)
with col2:
    col2.subheader('# álbumes')
    info_box(str(len(df['album'].unique())))
with col3:
    col3.subheader('Duración media')
    info_box(str(round(df['duration_ms'].mean(), 2)))

with col4:
    col4.subheader('# canciones por album')
    st.plotly_chart(canciones_por_album_chart, use_container_width=True)
with col5:
    col5.subheader('Top 10 Canciones Populares')
    st.plotly_chart(canciones_populares_chart, use_container_width=True)
with col6:
    col6.subheader('Relación Popularidad y Danceability')
    st.plotly_chart(relacion_popularidad_danceability_chart, use_container_width=True)
