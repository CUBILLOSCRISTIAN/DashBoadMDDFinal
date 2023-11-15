from graphene_django import DjangoObjectType
from graphene import ObjectType
from graphene import List, Int, String
from graphene import Schema

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
from .bigquery import DATA

class Query(ObjectType):
    anios2021 = List(Anios2021)
    anios2022 = List(Anios2022)
    anios2023 = List(Anios2023)
    departamento = List(Departamento)
    home = List(Home)
    region = List(Region)
    geoLocation = List(GeoLocation, location=String())
    municipios = List(Municipio)

    def resolve_anios2021(self, info):
        data = DATA.ANIOS2021
        return data

    def resolve_anios2022(self, info):
        data = DATA.ANIOS2022
        return data
    
    def resolve_anios2023(self, info):
        data = DATA.ANIOS2023
        return data

    def resolve_departamento(self, info):
        data = DATA.DEPARTAMENTO
        return data

    def resolve_home(self, info):
        data = DATA.HOME
        return data

    def resolve_region(self, info):
        data = DATA.REGION
        return data

    def resolve_geoLocation(self, info, location=None):
        data = DATA.GEOLOCATION
        if location:
            data = [*filter(lambda x: x.tipo == location, data)]
        return data

    def resolve_municipios(self, info):
        data = DATA.MUNICIPIOS
        return data
    
schema = Schema(query=Query)