from rest_framework import serializers

from .models import Check


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['order']
        required_fields = ['order']
