from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status

from receipt.serializers import OrderSerializer, CheckSerializer
from receipt.models import Check


class CreateChecksView(APIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        return Response({"ok": "Чеки успешно созданы"}, status=status.HTTP_200_OK)


class NewChecksView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CheckSerializer

    def get(self, request):
        data = request.query_params

        return Response(data, status=status.HTTP_200_OK)


class CheckView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CheckSerializer

    def get(self, request):
        data = request.query_params

        return Response(data, status=status.HTTP_200_OK)
