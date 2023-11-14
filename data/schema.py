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
    Region
)
from .bigquery import DATA

class Anios2021Type(ObjectType):
    class Meta:
        model = Anios2021
        fields = '__all__'

class Anios2022Type(ObjectType):
    class Meta:
        model = Anios2022
        fields = '__all__'

class Anios2023Type(ObjectType):
    class Meta:
        model = Anios2023
        fields = '__all__'

class DepartamentoType(ObjectType):
    class Meta:
        model = Departamento
        fields = '__all__'

class HomeType(ObjectType):
    class Meta:
        model = Home
        fields = '__all__'

class RegionType(ObjectType):
    class Meta:
        model = Region
        fields = '__all__'



class Query(ObjectType):
    anios2021 = List(Anios2021Type)
    anios2022 = List(Anios2022Type)
    anios2023 = List(Anios2023Type)
    departamento = List(DepartamentoType)
    home = List(HomeType)
    region = List(RegionType)

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
    
schema = Schema(query=Query)