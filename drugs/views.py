from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenViewBase

from drugs.models import Drug
from drugs.serializers import DrugSerializer


class DrugListCreateAPIView(ListCreateAPIView, TokenViewBase):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()


drug_list_create_view = DrugListCreateAPIView.as_view()


class DrugRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, TokenViewBase):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


drug_retrieve_update_delete_view = DrugRetrieveUpdateDestroyAPIView.as_view()
