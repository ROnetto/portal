from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drugs.models import Drug
from drugs.serializers import DrugSerializer


class DrugListCreateAPIView(ListCreateAPIView):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()

    permission_classes = [IsAuthenticated]


drug_list_create_view = DrugListCreateAPIView.as_view()


class DrugRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    permission_classes = [IsAuthenticated]


drug_retrieve_update_delete_view = DrugRetrieveUpdateDestroyAPIView.as_view()
