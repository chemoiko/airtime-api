from rest_framework import serializers  
from .models import Data
  
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['name','description']
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=100)