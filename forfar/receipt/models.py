from django.db import models
from django.conf import settings


# Константы типов чеков
CLIENT_CHECK = 'client'
KITCHEN_CHECK = 'kitchen'


# Константы статусов чеков
NEW = 'new'
RENDERED = 'rendered'
PRINTED = 'printed'


class Printer(models.Model):

    name = models.CharField(max_length=255, verbose_name='Наименование принтера')
    api_key = models.CharField(unique=True, max_length=32,
                               verbose_name='Ключ доступа к API')
    check_type = models.CharField(max_length=10, verbose_name='Тип чека')
    point_id = models.IntegerField(verbose_name='Идентификатор точки')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'
        db_table = 'printers'
        ordering = ['-id']


class Check(models.Model):

    def files_directory_path(instance, filename):
        filename = str(instance.order['id']) + '_' + str(instance.type) + '.pdf'
        return '{settings.PDF_CHECKS_PATH}{0}'.format(filename)

    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, 
                                   verbose_name='Принтер')
    type = models.CharField(max_length=10, verbose_name='Тип чека')
    order = models.JSONField(verbose_name='Информация о заказе')
    status = models.CharField(max_length=10, verbose_name='Статус чека')
    pdf_file = models.FileField(upload_to=files_directory_path,
                                blank=True, null=True, )

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    class Meta():
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        db_table = 'checks'
        ordering = ['-id']
