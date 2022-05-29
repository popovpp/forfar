from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import (NotFound, ValidationError,
                                       NotAuthenticated)
from django.template import Context, Template
from django.conf import settings
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist

from receipt.serializers import OrderSerializer
from receipt.models import (Check, Printer, CLIENT_CHECK, KITCHEN_CHECK,
                            NEW, RENDERED, PRINTED)
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
            raise NotFound(
                {"error": f'На точке с point_id={data["point_id"]} принтеры\
                 отсутствуют.'}
            )

        existing_checks = Check.objects.filter(order=data).all()
        if len(printers) == len(existing_checks):
            raise ValidationError(
                {"error":f'Чеки для заказа с id={data["id"]} уже сгнерированы.'}
            )
        
        context = set_context(data)
        for printer in printers:
            if printer.check_type == CLIENT_CHECK:
                check_template = Template(open(settings.CLIENT_CHECK).read())
            elif printer.check_type == KITCHEN_CHECK:
                check_template = Template(open(settings.KITCHEN_CHECK).read())
            check = set_check(data, printer)
            check.save()
            check_generator.delay(check_template.render(context), check)

        return Response({"ok": "Чеки успешно созданы"},
                        status=status.HTTP_200_OK)


class NewChecksView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = request.query_params

        if not getattr(data['api_key'], None):
            raise ValidationError(
                {"error":f'Параметр api_keq не передан'}
            )
        
        checks = Check.objects.select_related("printer_id").all()

        printers = Printer.objects.filter(api_key=str(data['api_key']))
        if not printers:
            raise NotAuthenticated({"error": "Ошибка авторизации"})

        new_checks = []
        for check in checks:
            if (check.status == RENDERED and 
                check.printer_id.api_key == str(data['api_key'])):
                new_checks.append({"id": check.id})
        output_data = {
            "checks": new_checks
        }

        return Response(output_data,
                        status=status.HTTP_200_OK)


class CheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = request.query_params

        try:
            check = Check.objects.select_related(
                                    "printer_id"
                                  ).get(id=data['check_id'])
        except ObjectDoesNotExist: 
            raise ValidationError(
                {"error":f'Чек с id={data["check_id"]} не существует.'}
            )

        printers = Printer.objects.filter(api_key=str(data['api_key']))
        if not printers:
            raise NotAuthenticated({"error": "Ошибка авторизации"})

        return FileResponse(open(check.pdf_file.path, "rb"),
                            as_attachment=True, filename=check.pdf_file.path)
