from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenViewBase

from vaccinations.models import Vaccination
from vaccinations.serializers import VaccinationSerializer


class VaccinationListCreateAPIView(ListCreateAPIView, TokenViewBase):
    serializer_class = VaccinationSerializer
    queryset = Vaccination.objects.all()


vaccination_list_create_view = VaccinationListCreateAPIView.as_view()


class VaccinationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, TokenViewBase):
    serializer_class = VaccinationSerializer
    queryset = Vaccination.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


vaccination_retrieve_update_delete_view = VaccinationRetrieveUpdateDestroyAPIView.as_view()

