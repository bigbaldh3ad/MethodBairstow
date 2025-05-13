from rest_framework import serializers
from .models import BairstowRegistro

class BairstowRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = BairstowRegistro
        fields = '__all__'
