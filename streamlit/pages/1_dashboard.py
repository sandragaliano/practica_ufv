import matplotlib
import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import requests
from matplotlib.backends.backend_agg import RendererAgg

@st.cache_data
def load_data(url: str):
    df = pd.read_csv('./taylor_swift_spotify.csv',sep=',')
    return df

def retrieve_data_post():
    try:
        response = requests.get('http://fastapi:8000/retrieve_data')
        if response.status_code == 200:
            df_dict = response.json()['songs']
            return pd.DataFrame(df_dict)
        else:
            raise ValueError(f"Error en la carga de datos: {response.text}")
    except Exception as e:
        st.error(f"Error en la carga de datos: {str(e)}")

def info_box(text, color=None):
    st.markdown(f'<div style="background-color:{color};opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{text}</p></div>', unsafe_allow_html=True)

df = load_data('http://fastapi:8000/retrieve_data')

registros = str(df.shape[0])

# Gráfica 1: Canciones por álbum

# Elemento de filtro para seleccionar un álbum y hacer la gráfica interactiva
album_seleccionado = st.selectbox('Selecciona un álbum:', df['album'].unique())

# Diccionario de colores personalizados para cada álbum
color_map = {
    "1989 (Taylor's Version) [Deluxe]": 'lightseagreen',
    "1989 (Taylor's Version)": 'lightseagreen',
    '1989 (Deluxe Edition)': 'lightseagreen',
    'Midnights (The Til Dawn Edition)': 'midnightblue',
    'Midnights (3am Edition)': 'midnightblue',
    'Midnights': 'midnightblue',
    'Lover': 'pink',
    '1989': 'cyan',
    'Red': 'maroon',
    'Red (Deluxe Edition)': 'maroon',
    'reputation': 'black',
    'reputation Stadium Tour Surprise Song Playlist': 'black',
    'Speak Now World Tour Live': 'mediumpurple',
    'Speak Now': 'mediumpurple',
    'Speak Now (Deluxe Edition)': 'mediumpurple',
    "Speak Now (Taylor's Version)": "mediumpurple",
    "Red (Taylor's Version)": 'maroon',
    "Fearless Platinum Edition": 'burlywood',
    "Fearless": 'burlywood',
    "Live From Clear Channel Stripped 2008": 'burlywood',
    "Taylor Swift": 'seagreen',
    "Fearless (Taylor's Version)": "burlywood",
    "evermore (deluxe version)": 'darkgoldenrod',
    'evermore': 'darkgoldenrod',
    "folklore": 'silver',
    'folklore (deluxe version)': 'silver',
    'folklore: the long pond studio sessions (from the Disney+ special)[deluxe edition]': 'silver'}

# Filtrar el DataFrame por el álbum seleccionado para la gráfica de barras
canciones_por_album = df[df['album'] == album_seleccionado][['name', 'popularity']]
canciones_por_album_chart = px.bar(
    canciones_por_album, x='name', y='popularity',
    labels={'name': 'Canción', 'popularity': 'Popularidad'},
)

# Modificar el color de las barras según el álbum seleccionado
color_album = color_map.get(album_seleccionado, 'blue')
canciones_por_album_chart.update_traces(marker_color=color_album)

# Gráfica 2: Top 10 Canciones Populares como Pie Chart
# Usamos las 10 canciones con mayor número de popularidad:
canciones_populares = df.nlargest(10, 'popularity')[['name', 'popularity', 'album']]
# Agregamos una columna de colores basada en el álbum
canciones_populares['color'] = canciones_populares['album'].map(color_map)

# Gráfico de pie chart de las 10 con mayor popularidad:
canciones_populares_chart = px.pie(
    canciones_populares, names='name', values='popularity',
    color=canciones_populares['color'].tolist(),  # Utilizamos la columna de colores
    labels={'name': 'Canción', 'popularity': 'Popularidad'}
)

# Configuramos la leyenda
canciones_populares_chart.update_layout(
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
)

# Seleccionamos un color por cada categoría para la leyenda
canciones_populares_chart.update_traces(
    hoverinfo='label+percent',
    textinfo='value',
    textfont_size=14,
)


# Gráfica 3: Relación Popularidad y Danceability
# Relación popularidad - danceability (son las canciones más bailables las más populares??)
relacion_popularidad_danceability_chart = px.scatter(
    df, x='popularity', y='danceability',
    labels={'popularity': 'Popularidad', 'danceability': 'Danceability'}
)

sns.set_palette("pastel")

# Título
st.subheader("Taylor Swift: Person of the Year")

col4, col5, col6 = st.columns(3)
with col4:
    st.subheader('# canciones')
    info_box(registros)

with col5:
    st.subheader('# álbumes')
    info_box(str(len(df['album'].unique())))

with col6:
    st.subheader('Duración media')
    info_box(str(round(df['duration_ms'].mean(), 2)))

# Col1: Gráfica de Barras
st.subheader(f'Popularidad de Canciones por Álbum ({album_seleccionado})')
st.plotly_chart(canciones_por_album_chart, use_container_width=True)

# Col2 y Col3: Gráfica de Pie y Scatter
col2, col3 = st.columns(2)
with col2:
    st.subheader('Top 10 Canciones Populares')
    st.plotly_chart(canciones_populares_chart, use_container_width=True)

with col3:
    st.subheader('Relación Popularidad y Danceability')
    st.plotly_chart(relacion_popularidad_danceability_chart, use_container_width=True)