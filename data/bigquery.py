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
    Region
)


class Data():
    def __init__(self):
        self.PROJECT = 'proyectofinal-404415'
        self.DATASET = 'project'

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
    
    def get_anios2021(self):
        sql = """
            SELECT *
            FROM `{}.anios2021`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        anios2021 = [
            Anios2021(
                fecha = data['fecha'],
                mediaViento = data['mediaViento']
            ) for i, data in df_data.iterrows()
        ]
        return anios2021
    
    def get_anios2022(self):
        sql = """
            SELECT *
            FROM `{}.anios2022`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        anios2022 = [
            Anios2022(
                fecha = data['fecha'],
                mediaViento = data['mediaViento']
            ) for i, data in df_data.iterrows()
        ]
        return anios2022
    
    def get_anios2023(self):
        sql = """
            SELECT *
            FROM `{}.anios2023`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        anios2023 = [
            Anios2023(
                fecha = data['fecha'],
                mediaViento = data['mediaViento']
            ) for i, data in df_data.iterrows()
        ]
        return anios2023
    
    def get_departamento(self):
        sql = """
            SELECT *
            FROM `{}.departamento`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        departamento = [
            Departamento(
                nombre = data['nombre'],
                cantidadEstaciones = data['cantidadEstaciones'],
                media = data['media'],
                mediana = data['mediana']
            ) for i, data in df_data.iterrows()
        ]
        return departamento

    def get_home(self):
        sql = """
            SELECT *
            FROM `{}.home`
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
            FROM `{}.region`
        """.format(self.DATASET)
        df_data = self.client.query(sql).result().to_dataframe()

        region = [
            Region(
                region = data['region'],
                medVel = data['medVel'],
                avgVel = data['avgVel'],
                medDir = data['medDir'],
                avgDir = data['avgDir'],
                noEstaciones = data['noEstaciones']
            ) for i, data in df_data.iterrows()
        ]
        return region

DATA = Data()