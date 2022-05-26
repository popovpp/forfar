from rest_framework import serializers

from .models import Check


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ['order']


class CheckSerializer(serializers.ModelSerializer):
	class Meta:
		model = Check
		fields = ['id', 'printer_id', 'type', 'order', 'status', 'pdf_file']
