from django.views.generic import TemplateView, FormView
from django.conf import settings
from numpy import array
import joblib, os, ast

from data.schema import schema
from .utils import (
    generate_anios_graph,
    generate_region_media_mediana_graph,
    generate_region_estaciones_velocidad_graph,
    generate_region_map_graph,
    generate_departamento_media_mediana_graph,
    generate_departamento_estaciones_velocidad_graph,
    generate_region_rose_diagram,
    generate_departamento_rose_diagram,
    generate_departamento_map_graph,
    get_municipios
)
from .forms import FormPrediction

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
        region_rose_graph = generate_region_rose_diagram(result_, 'region_rose')
        
        kwargs.update({
            'region_media_mediana_url': region_media_mediana_graph,
            'region_media_estaciones_url': region_media_estaciones_graph,
            'region_map_url': region_map_graph,
            'region_rose_url': region_rose_graph,
        })
        
        return super().get_context_data(**kwargs)


class DepartamentoDataView(TemplateView):
    template_name = 'service/departamento.html'

    def get_context_data(self, **kwargs):

        query = """
            {
                departamento{
                    nombre
                    medVel
                    avgVel
                    medDir
                    avgDir
                    noEstaciones
                }
            }
        """
        result_ = schema.execute(query).data['departamento']
        query = """
            {
                geoLocation(location: "departamento"){
                    nombre
                    propiedades
                }
            }
        """
        geoResult_ = schema.execute(query).data['geoLocation']

        departamento_media_mediana_graph = generate_departamento_media_mediana_graph(result_, 'departamento_media_mediana')
        departamento_media_estaciones_graph = generate_departamento_estaciones_velocidad_graph(result_, 'departamento_media_estaciones')
        departamento_map_graph = generate_departamento_map_graph(result_, geoResult_, 'departamento_map')
        departamento_rose_graph = generate_departamento_rose_diagram(result_, 'departamento_rose')

        kwargs.update({
            'departamento_media_mediana_url': departamento_media_mediana_graph,
            'departamento_media_estaciones_url': departamento_media_estaciones_graph,
            'departamento_map_url': departamento_map_graph,
            'departamento_rose_url': departamento_rose_graph
        })
        
        return super().get_context_data(**kwargs)


class ForescatingView(FormView):
    template_name = 'service/forescating.html'
    form_class = FormPrediction

    query = """
        {
            municipios{
                nombre
                latitud
                longitud
                codigo
            }
        }
    """
    result_ = schema.execute(query).data['municipios']
    municipios = get_municipios(result_)
    form = FormPrediction(municipios)

    def get_context_data(self, form=form, entrada=[], **kwargs):
        solution = ''
        url = os.path.join(settings.BASE_DIR, 'static/models/model_predict_hour_1.pkl')
        if entrada: 
            model = joblib.load(url)
            solution = model._Booster.predict(array(entrada).reshape(1,-1))[0]
        kwargs.update({
            'form': form,
            'solution': f'Para una latitud {entrada[0][0]} y longitud {entrada[0][1]} predecimos una velocidad de {solution} m/s' if solution else ''
        })
        return super().get_context_data(**kwargs)
    
    def post(self, request, *args, **kwargs):
        form = FormPrediction(self.municipios, request.POST)
        if form.is_valid():
            lugar = ast.literal_eval(form.cleaned_data['lugar'])
            velocidad = form.cleaned_data['velocidad']
            return self.render_to_response(self.get_context_data(form=form, entrada=[lugar + [velocidad]]))
        return self.render_to_response(self.get_context_data(form=form))