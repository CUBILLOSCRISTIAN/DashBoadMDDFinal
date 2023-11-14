from plotly.express import bar, bar_polar, choropleth_mapbox
from plotly.express.colors import sequential
from pandas import DataFrame
from django.conf import settings
from plotly.offline import plot
import plotly.express as px
import json, os
import pandas as pd

def df_to_geojson(df):
    df = DataFrame(df)
    geojson = {'type': 'FeatureCollection', 'features': []}

    for i, element in df.iterrows():
        feature = {
            'type': 'Feature', 
            'properties': {},
            'geometry': {}
        }
        
        feature['geometry'] = json.loads(element['propiedades'])
        if 'Nariño' in element['name']:
                feature['properties']['name'] = 'Narino'
        if 'san andres' in element['name']:
                feature['properties']['name'] = 'San andres'
        elif 'bogota' in element['name']:
            feature['properties']['name'] = 'Bogota d.c'
        else:
            feature['properties']['name'] = element['nombre']
        geojson['features'].append(feature)
    return geojson

def generate_region_map_graph(data, geoData, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'
    df = DataFrame(data)
    df['region'] = df['region'].str.capitalize()
    df.loc[df['region'] == 'Insular', 'region'] = 'Caribe'
    df = df.groupby('region', as_index=False)['medVel'].mean()
    
    fig = px.choropleth_mapbox(
        geojson = df_to_geojson(geoData),
        locations = 'region',
        featureidkey = 'properties.name',
        color = 'medVel',
        color_continuous_scale='Plasma',
        range_color = (df['medVel'].min(), df['medVel'].max()),
        mapbox_style = "carto-positron",
        zoom = 4.4,
        center = {"lat": 4.0, "lon": -73.0},
        opacity=  0.5,
        labels = {'medVel': 'VELOCIDAD (m/s)'}
    )

    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_departamento_media_mediana_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'nombre': 'DEPARTAMENTO', 'cantidadEstaciones': 'CANTIDAD ESTACIONES', 'avgVel': 'MEDIA', 'medVel': 'MEDIANA'}, inplace=True)
    df_long = pd.melt(df, id_vars=['DEPARTAMENTO'], value_vars=['MEDIA', 'MEDIANA'],
                  var_name='estadistica', value_name='valor')

    # Crea el gráfico de barras
    fig = px.bar(
        df_long,
        x="DEPARTAMENTO",
        y="valor",
        color="estadistica",
        barmode='group',  # Agrupa las barras para cada departamento
        labels={'valor': 'Velocidad', 'DEPARTAMENTO': 'Departamentos'},
        title='Comparación de Media y Mediana por Departamento'
    )

    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_departamento_estaciones_velocidad_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'nombre': 'DEPARTAMENTO', 'noEstaciones': 'CANTIDAD ESTACIONES', 'avgVel': 'MEDIA', 'medVel': 'MEDIANA'}, inplace=True)
    df_long = pd.melt(df, id_vars=['DEPARTAMENTO'], value_vars=['MEDIA', 'CANTIDAD ESTACIONES'],
                  var_name='estadistica', value_name='valor')

    # Crea el gráfico de barras
    fig = px.bar(
        df_long,
        x="DEPARTAMENTO",
        y="valor",
        color="estadistica",
        barmode='group',  # Agrupa las barras para cada departamento
        labels={'valor': 'Velocidad vs Estaciones', 'DEPARTAMENTO': 'Departamentos'},
        title='Comparación de Media y Cantidad de estaciones por Departamento'
    )
    
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_region_estaciones_velocidad_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'region': 'REGION', 'noEstaciones': 'CANTIDAD ESTACIONES', 'avgVel': 'MEDIA', 'medVel': 'MEDIANA'}, inplace=True)
    df_long = pd.melt(df, id_vars=['REGION'], value_vars=['MEDIA', 'CANTIDAD ESTACIONES'],
                  var_name='estadistica', value_name='valor')

    # Crea el gráfico de barras
    fig = px.bar(
        df_long,
        x="REGION",
        y="valor",
        color="estadistica",
        barmode='group',  # Agrupa las barras para cada departamento
        labels={'valor': 'Velocidad vs Estaciones', 'REGION': 'Región'},
        title='Comparación de Media y Cantidad de estaciones por Región'
    )
    
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_region_media_mediana_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'region': 'REGION', 'noEstaciones': 'CANTIDAD ESTACIONES', 'avgVel': 'MEDIA', 'medVel': 'MEDIANA'}, inplace=True)
    df_long = pd.melt(df, id_vars=['REGION'], value_vars=['MEDIA', 'MEDIANA'],
                  var_name='estadistica', value_name='valor')

    # Crea el gráfico de barras
    fig = px.bar(
        df_long,
        x="REGION",
        y="valor",
        color="estadistica",
        barmode='group',  # Agrupa las barras para cada departamento
        labels={'valor': 'Velocidad', 'REGION': 'Región'},
        title='Comparación de Media y Mediana por Región'
    )

    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_anios_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'fecha': 'Fecha', 'mediaViento': 'Velocidad Media'}, inplace=True)

    fig = px.line(
        df,
        x="Fecha",
        y="Velocidad Media"
    )

    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'