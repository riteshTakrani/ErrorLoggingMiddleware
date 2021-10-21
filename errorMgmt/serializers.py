from rest_framework import serializers
from .models import ResponseModel


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResponseModel
        fields = ['id', 'status', 'error', 'entry_date']
