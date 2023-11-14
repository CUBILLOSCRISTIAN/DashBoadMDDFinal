from plotly.express.colors import sequential
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from django.conf import settings
from plotly.offline import plot
from pandas import DataFrame
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
        feature['properties']['name'] = element['nombre']
        if 'Nariño' in element['nombre']:
                feature['properties']['name'] = 'Narino'
        if 'san andres' in element['nombre']:
                feature['properties']['name'] = 'San andres'
        if 'bogota' in element['nombre']:
            feature['properties']['name'] = 'Bogota'
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
        df, 
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

def generate_region_estaciones_velocidad_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'region': 'REGION', 'noEstaciones': 'CANTIDAD ESTACIONES', 'avgVel': 'MEDIA', 'medVel': 'MEDIANA'}, inplace=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Crea el gráfico de barras
    fig.add_trace(go.Bar(x=df['REGION'], y=df['MEDIA'], name="Viento medio", offsetgroup=1), secondary_y=False)
    fig.add_trace(go.Bar(x=df['REGION'], y=df['CANTIDAD ESTACIONES'], name="Cantidad de estaciones", offsetgroup=2), secondary_y=True)
    
    fig.update_layout(
        title="Comparación de Media y Cantidad de estaciones por Región",
        xaxis_title="Región",
        yaxis=dict(title="Viento medio"),
        yaxis2=dict(title="Cantidad de estaciones", overlaying="y", side="right"),bargap=0.4
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

def generate_region_rose_diagram(data, name):
    DIRECTIONS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    data = [*map(lambda x: {'name': x['region'], 'medianSpeed': x['medVel'], 'medianDirection': DIRECTIONS[(int((x['medDir']/22.5) + .5) % 16)]}, data)]
    data += [{'name': '', 'medianSpeed': 0, 'medianDirection': d} for d in DIRECTIONS]
    data = [tuple for x in DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
    df = DataFrame(data)
    df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad (m/s)', 'medianDirection': 'Dirección'}, inplace=True)        
    fig = px.bar_polar(
        df, 
        r='Velocidad (m/s)', 
        theta='Dirección', 
        color='Nombre', 
        color_discrete_sequence=sequential.Plasma_r
    )
    fig.update_layout(
            font = dict(
                family = "Merriweather",
                size = 15
            ),
            legend = dict(
                title = None,
                orientation = "v"
            ),
            margin=dict(l=20, r=20, b=20, t=20)
        )
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'