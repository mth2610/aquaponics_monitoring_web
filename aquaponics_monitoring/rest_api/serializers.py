from models import Sites
from rest_framework import serializers

class SiteSerializer(serializers.Serializer):
    site_code = serializers.JSONField(required=True)
    sensors = serializers.JSONField(required=True)
    fish_tanks = serializers.JSONField(required=True)

class DataValueSerializer(serializers.Serializer):
    site_code = serializers.JSONField(required=True)
    sensor_code = serializers.JSONField(required=True)
    datetime = serializers.DateTimeField(required=True)
    value = serializers.FloatField(required=True)

class ImageSerializer(serializers.Serializer):
    site_code = serializers.JSONField(required=True)
    path = serializers.JSONField(required=True)
    datetime = serializers.DateTimeField(required=True)
