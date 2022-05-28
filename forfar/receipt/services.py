from django_rq import job
from django.template import Context
import json
import requests

from receipt.models import (CLIENT_CHECK, KITCHEN_CHECK, NEW, RENDERED,
	                 PRINTED, Check)

@job
def check_generator(check_template):
    
	url = 'http://localhost:80/'

	data = {
	    'contents': check_template,#.encode('utf8'),
	}
	headers = {
	    'Content-Type': 'application/json',    # This is important
	}
	response = requests.post(url, data=data)#, headers=headers)

	# Save the response contents to a file
	with open('media/pdf/file.pdf', 'wb') as f:
	    f.write(response.content)


def set_context(data):
	return Context({
		'order_id': data['id'],
        'order_address': data['address'],
        'products': data['items'],
        'client_name': data['client']['name'],
        'client_phone': data['client']['phone'],
        'check_price': data['price']
	})


def set_check(data, printer, check_type):

	return Check(
        printer_id = printer,
        type = check_type,
        order = data,
        status = NEW,
        pdf_file = None
	)
