from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rut_chile import rut_chile

from django.utils.translation import ugettext_lazy as _

from drugs.serializers import DrugSerializer
from vaccinations.models import Vaccination


class VaccinationSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    drug_id = serializers.IntegerField(write_only=True)

    def validate_dose(self, dose):
        minimum = Decimal('0.15')
        maximum = Decimal('1.0')
        if not minimum <= dose <= maximum:
            raise ValidationError(_("Invalid dose. Value must be between 0.15 and 1.0"))
        return dose

    def validate_rut(self, rut):
        if not rut_chile.is_valid_rut(rut):
            raise ValidationError(_("Invalid rut"))
        return rut

    class Meta:
        model = Vaccination
        fields = ['rut', 'dose', 'date', 'drug', 'drug_id']
