from rest_framework.serializers import Serializer
from rest_framework import serializers


class MovieSerializer(Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()
