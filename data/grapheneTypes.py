import graphene

class Anios2021(graphene.ObjectType):
    fecha = graphene.DateTime()
    mediaViento  = graphene.Float()


class Anios2022(graphene.ObjectType):
    fecha = graphene.DateTime()
    mediaViento  = graphene.Float()

class Anios2023(graphene.ObjectType):
    fecha = graphene.DateTime()
    mediaViento  = graphene.Float()


class Departamento(graphene.ObjectType):
    nombre = graphene.String()
    medVel  = graphene.Float()
    avgVel = graphene.Float()
    medDir = graphene.Float()
    avgDir = graphene.Float()
    noEstaciones = graphene.Int()

class Home(graphene.ObjectType):
    media = graphene.Float()
    mediana = graphene.Float()
    cantMunicipio = graphene.Int()
    canDepartamento = graphene.Int()
    cantRegion = graphene.Int()
    cantEstacion = graphene.Int()
    cantRegistros = graphene.Int()

class Region(graphene.ObjectType):
    region = graphene.String()
    medVel  = graphene.Float()
    avgVel = graphene.Float()
    medDir = graphene.Float()
    avgDir = graphene.Float()
    noEstaciones = graphene.Int()

class GeoLocation(graphene.ObjectType):
    propiedades = graphene.JSONString()
    nombre = graphene.String()
    tipo = graphene.String()