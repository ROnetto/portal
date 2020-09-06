from rest_framework import serializers

from drugs.models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['name', 'code', 'description']
