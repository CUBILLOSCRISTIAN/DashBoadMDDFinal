from google.oauth2 import service_account
from google.cloud import bigquery
from django.conf import settings
import os, json

from .grapheneTypes import (
    Anios2021,
    Anios2022,
    Anios2023,
    Departamento,
    Home,
    Region,
    GeoLocation,
    Municipio
)


class Data():
    def __init__(self):
        self.PROJECT = 'proyectofinal-404415'
        self.DATASET = 'WindsForecast'

        key = os.path.join(settings.BASE_DIR, 'static/key.json')
        credential = service_account.Credentials.from_service_account_file(key)
        self.client = bigquery.Client(
            credentials = credential,
            project = self.PROJECT
        )

        self.ANIOS2021 = self.get_anios2021()
        self.ANIOS2022 = self.get_anios2022()
        self.ANIOS2023 = self.get_anios2023()
        self.DEPARTAMENTO = self.get_departamento()
        self.HOME = self.get_home()
        self.REGION = self.get_region()
        self.GEOLOCATION = self.get_geo_region()
        self.MUNICIPIOS = self.get_municipios()
    
    def get_anios2021(self):
        sql = """
            SELECT *
            FROM `{}.Años2021`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        anios2021 = [
            Anios2021(
                fecha = data['Fecha'],
                mediaViento = data['MediaViento']
            ) for i, data in df_data.iterrows()
        ]
        return anios2021
    
    def get_anios2022(self):
        sql = """
            SELECT *
            FROM `{}.Años2022`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        anios2022 = [
            Anios2022(
                fecha = data['Fecha'],
                mediaViento = data['MediaViento']
            ) for i, data in df_data.iterrows()
        ]
        return anios2022
    
    def get_anios2023(self):
        sql = """
            SELECT *
            FROM `{}.Años2023`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        anios2023 = [
            Anios2023(
                fecha = data['Fecha'],
                mediaViento = data['MediaViento']
            ) for i, data in df_data.iterrows()
        ]
        return anios2023
    
    def get_departamento(self):
        sql = """
            SELECT *
            FROM `{}.Departamentos`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        departamento = [
            Departamento(
                nombre = data['Departamento'],
                medVel = data['MedianaVelocidad'],
                avgVel = data['MediaVelocidad'],
                medDir = data['MedianaDireccion'],
                avgDir = data['MediaDireccion'],
                noEstaciones = data['CantidadEstaciones']
            ) for i, data in df_data.iterrows()
        ]
        return departamento

    def get_home(self):
        sql = """
            SELECT *
            FROM `{}.Home`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        home = [
            Home(
                media = data['media'],
                mediana = data['mediana'],
                cantMunicipio = data['cantMunicipio'],
                canDepartamento = data['canDepartamento'],
                cantRegion = data['cantRegion'],
                cantEstacion = data['cantEstacion'],
                cantRegistros = data['cantRegistros']
            ) for i, data in df_data.iterrows()
        ]
        return home

    def get_region(self):
        sql = """
            SELECT *
            FROM `{}.Region`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        region = [
            Region(
                region = data['Region'],
                medVel = data['MedianaVelocidad'],
                avgVel = data['MediaVelocidad'],
                medDir = data['MedianaDireccion'],
                avgDir = data['MediaDireccion'],
                noEstaciones = data['NumeroEstaciones']
            ) for i, data in df_data.iterrows()
        ]
        return region

    def get_geo_region(self):
        sql = """
            SELECT *
            FROM `{}.geo_region`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()
        geo_locacion = [
            GeoLocation(
                nombre = data['REGION'],
                propiedades = json.loads(data['GEOMETRY']),
                tipo = 'region'
            ) for i, data in df_data.iterrows()
        ]

        sql = """
            SELECT *
            FROM `{}.geo_department`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()
        geo_locacion += [
            GeoLocation(
                nombre = data['DEPARTMENT'],
                propiedades = json.loads(data['GEOMETRY']),
                tipo = 'departamento'
            ) for i, data in df_data.iterrows()
        ]
        return geo_locacion

    def get_municipios(self):
        sql = """
            SELECT *
            FROM `{}.Municipios`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        region = [
            Municipio(
                codigo = data['Codigo'],
                latitud = data['Latitud'],
                longitud = data['Longitud'],
                nombre = data['Municipio']
            ) for i, data in df_data.iterrows()
        ]
        return region

DATA = Data()