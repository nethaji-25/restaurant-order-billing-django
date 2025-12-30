from rest_framework import serializers
from .models import Empdetails

class Serializer(serializers.ModelSerializer):
    class Meta:
        model=Empdetails
        fields='__all__'