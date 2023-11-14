from django.views.generic import TemplateView

from data.schema import schema

from .utils import (
    generate_departamento_graph,
    generate_region_graph,
)

class GeneralDataView(TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, **kwargs):

        query = """
            {
                Home{
                    cantMunicipio
                    canDepartamento
                    cantRegion
                    cantEstacion
                    cantRegistros
                }
            }
        """

        result_ = schema.execute(query).data['Home']

        query = """
            {
                Anios2021{
                    fecha
                    mediaViento
                }
            }
        """

        Anios2021result_ = schema.execute(query).data['Anios2021']

        query = """
            {
                Anios2022{
                    fecha
                    mediaViento
                }
            }
        """

        Anios2022result_ = schema.execute(query).data['Anios2022']

        query = """
            {
                Anios2023{
                    fecha
                    mediaViento
                }
            }
        """

        Anios2023result_ = schema.execute(query).data['Anios2023']

        query = """
            {
                Departamento{
                    departamento
                    cantidadEstaciones
                    mediaVelocidad
                    medianaVelocidad
                    mediaDireccion
                    medianaDireccion
                }
            }
        """
        departamentoResult_ = schema.execute(query).data['Departamento']

        query = """
            {
                Region{
                    region
                    medVel
                    avgVel
                    medDir
                    avgDir
                    noEstaciones
                }
            }
        """
        regionResult_ = schema.execute(query).data['Region']
        

        departamento_graph = generate_departamento_graph(departamentoResult_, 'departamento')
        region_graph = generate_region_graph(regionResult_, 'region')
        
        kwargs.update({
            'cantMunicipio': result_['cantMunicipio'],
            'canDepartamento': result_['canDepartamento'],
            'cantRegion': result_['cantRegion'],
            'cantEstacion': result_['cantEstacion'],
            'cantRegistros': result_['cantRegistros'],

            'departamento_graph': departamento_graph,
            'region_graph': region_graph,
        })
        
        return super().get_context_data(**kwargs)


