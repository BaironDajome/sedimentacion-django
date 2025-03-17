from rest_framework import serializers
from .models import ShapefileData

class ShapefileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShapefileData
        fields = "__all__"
