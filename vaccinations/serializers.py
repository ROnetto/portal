from rest_framework import serializers

from drugs.serializers import DrugSerializer
from vaccinations.models import Vaccination


class VaccinationSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    drug_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Vaccination
        fields = ['rut', 'dose', 'date', 'drug', 'drug_id']
