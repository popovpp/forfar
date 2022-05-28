from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from django.template import Context, Template
from django.conf import settings

from receipt.serializers import OrderSerializer, CheckSerializer
from receipt.models import Check, Printer, CLIENT_CHECK, KITCHEN_CHECK, NEW, RENDERED, PRINTED
from receipt.services import set_check, set_context, check_generator


class CreateChecksView(APIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data['order']

        printers = Printer.objects.filter(point_id=data['point_id']).all()
        if not printers:
            raise NotFound(f'На точке с point_id={data["point_id"]} принтеры отсутствуют.')

        existing_checks = Check.objects.filter(order=data).all()
        if len(printers) == len(existing_checks):
            raise ValidationError(f'Чеки для заказа с id={data["id"]} уже сгнерированы.')
        
        context = set_context(data)
        for printer in printers:
            if printer.check_type == CLIENT_CHECK:
                check = set_check(data, printer, CLIENT_CHECK)
                check_template = Template(open(settings.CLIENT_CHECK).read())
            elif printer.check_type == KITCHEN_CHECK:
                check = set_check(data, printer, KITCHEN_CHECK)
                check_template = Template(open(settings.KITCHEN_CHECK).read())
            check_generator.delay(check_template.render(context))
            check.save()

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
