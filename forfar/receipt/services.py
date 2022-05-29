from django_rq import job
from django.template import Context
import json
import requests
from django.core.files import File

from receipt.models import (CLIENT_CHECK, KITCHEN_CHECK, NEW, RENDERED,
	                 PRINTED, Check)
from django.conf import settings

@job
def check_generator(check_template, check):
    
    url = settings.WKHTMLTOPDF_URL

    fp = bytes(check_template.encode('utf8'))
    files = {'file': fp}
    response = requests.post(url, files=files)
    
    filename = str(check.order['id']) + '_' + check.type + '.pdf'

    with open(settings.MEDIA_ROOT + '/' + settings.PDF_CHECKS_PATH +
              filename, 'wb') as f:
        f.write(response.content)
        check.pdf_file = settings.PDF_CHECKS_PATH + filename
        check.status = RENDERED
        check.save()


def set_context(data):
	return Context({
		'order_id': data['id'],
        'order_address': data['address'],
        'products': data['items'],
        'client_name': data['client']['name'],
        'client_phone': data['client']['phone'],
        'check_price': data['price']
	})


def set_check(data, printer):

	return Check(
        printer_id = printer,
        type = printer.check_type,
        order = data,
        status = NEW,
        pdf_file = None
	)
