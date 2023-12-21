import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns

@st.cache_data
def load_data():
    # Cargar conjunto de datos de Taylor Swift
    df = pd.read_csv('/home/sandra/repositorios/repos/practica_ufv/streamlit/pages/taylor_swift_spotify.csv', sep=',')
    return df


def info_box(texto, color=None):
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{texto}</p></div>', unsafe_allow_html=True)

df = load_data()
registros = str(df.shape[0])

# Gráfica 1: Canciones por álbum

# Elemento de filtro para seleccionar un álbum
album_seleccionado = st.selectbox('Selecciona un álbum:', df['album'].unique())
# Crear un diccionario de mapeo de colores para cada álbum
color_map = {album: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, album in enumerate(df['album'].unique())}
# Filtrar el DataFrame por el álbum seleccionado para la gráfica de barras
canciones_por_album = df[df['album'] == album_seleccionado][['name', 'popularity']]
canciones_por_album_chart = px.bar(
    canciones_por_album, x='name', y='popularity',
    color_discrete_map={album_seleccionado: color_map[album_seleccionado]},
    title=f'Popularidad de Canciones por Álbum ({album_seleccionado})',
    labels={'name': 'Canción', 'popularity': 'Popularidad'},
)

# Gráfica 2: Top 10 Canciones Populares como Pie Chart
# Usamos las 10 canciones con mayor número de popularidad:
canciones_populares = df.nlargest(10, 'popularity')[['name', 'popularity']]
# Gráfico de pie de las 10 con mayor popularidad:
canciones_populares_chart = px.pie(
    canciones_populares, names='name', values='popularity',
    labels={'name': 'Canción', 'popularity': 'Popularidad'}
)

# Configuración de diseño para la leyenda y visibilidad del pie chart
canciones_populares_chart.update_layout(
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0)
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
