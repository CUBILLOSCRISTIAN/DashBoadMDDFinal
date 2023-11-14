from django.urls import path

from .views import GeneralDataView, RegionDataView, DepartamentoDataView

urlpatterns = [
    path('', GeneralDataView.as_view(), name='home'),
    path('region', RegionDataView.as_view(), name='region'),
    path('departamento', DepartamentoDataView.as_view(), name='departamento'),
]
