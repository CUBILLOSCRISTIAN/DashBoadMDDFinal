from django.views.generic import TemplateView

from data.schema import schema

from .utils import (
    generate_anios_graph,
    generate_region_media_mediana_graph,
    generate_region_estaciones_velocidad_graph,
    generate_region_map_graph,
)

class GeneralDataView(TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, **kwargs):

        query = """
            {
                home{
                    cantMunicipio
                    canDepartamento
                    cantRegion
                    cantEstacion
                    cantRegistros
                }
            }
        """
        result_ = schema.execute(query).data['home'][0]

        query = """
            {
                anios2021{
                    fecha
                    mediaViento
                }
            }
        """
        Anios2021result_ = schema.execute(query).data['anios2021']

        query = """
            {
                anios2022{
                    fecha
                    mediaViento
                }
            }
        """
        Anios2022result_ = schema.execute(query).data['anios2022']

        query = """
            {
                anios2023{
                    fecha
                    mediaViento
                }
            }
        """
        Anios2023result_ = schema.execute(query).data['anios2023']

        anios2021 = generate_anios_graph(Anios2021result_, 'anios2021')
        anios2022 = generate_anios_graph(Anios2022result_, 'anios2022')
        anios2023 = generate_anios_graph(Anios2023result_, 'anios2023')
        
        kwargs.update({
            'cantMunicipio': result_['cantMunicipio'],
            'canDepartamento': result_['canDepartamento'],
            'cantRegion': result_['cantRegion'],
            'cantEstacion': result_['cantEstacion'],
            'cantRegistros': result_['cantRegistros'],

            'anios_2021_url': anios2021,
            'anios_2022_url': anios2022,
            'anios_2023_url': anios2023
        })
        
        return super().get_context_data(**kwargs)


class RegionDataView(TemplateView):
    template_name = 'service/region.html'

    def get_context_data(self, **kwargs):

        query = """
            {
                region{
                    region
                    medVel
                    avgVel
                    medDir
                    avgDir
                    noEstaciones
                }
            }
        """
        result_ = schema.execute(query).data['region']
        query = """
            {
                geoLocation(location: "region"){
                    nombre
                    propiedades
                }
            }
        """
        geoResult_ = schema.execute(query).data['geoLocation']

        region_media_mediana_graph = generate_region_media_mediana_graph(result_, 'region_media_mediana')
        region_media_estaciones_graph = generate_region_estaciones_velocidad_graph(result_, 'region_media_estaciones')
        region_map_graph = generate_region_map_graph(result_, geoResult_, 'region_map')
        
        kwargs.update({
            'region_media_mediana_url': region_media_mediana_graph,
            'region_media_estaciones_url': region_media_estaciones_graph,
            'region_map_url': region_map_graph,
        })
        
        return super().get_context_data(**kwargs)