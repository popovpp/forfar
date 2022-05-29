from django.contrib import admin

from .models import Printer, Check


class PrinterModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'api_key', 'check_type', 'point_id']
    list_display_links = ['id']
    list_filter = ['name', 'api_key', 'check_type', 'point_id']
    search_fields = ['name', 'api_key', 'check_type', 'point_id']

    class Meta:
        model = Printer


class CheckModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'printer_id', 'type', 'order', 'status', 'pdf_file']
    list_display_links = ['id']
    list_filter = ['printer_id', 'type', 'status']
    search_fields = ['printer_id', 'type', 'order', 'status', 'pdf_file']

    class Meta:
        model = Check


admin.site.register(Printer, PrinterModelAdmin)
admin.site.register(Check, CheckModelAdmin)
