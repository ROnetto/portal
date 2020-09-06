from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from vaccinations.models import Vaccination
from vaccinations.serializers import VaccinationSerializer


class VaccinationListCreateAPIView(ListCreateAPIView):
    serializer_class = VaccinationSerializer
    queryset = Vaccination.objects.all()

    # permission_classes = [IsAuthenticated]


vaccination_list_create_view = VaccinationListCreateAPIView.as_view()


class VaccinationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = VaccinationSerializer
    queryset = Vaccination.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    # permission_classes = [IsAuthenticated]


vaccination_retrieve_update_delete_view = VaccinationRetrieveUpdateDestroyAPIView.as_view()

