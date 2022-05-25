from django.db import models


class Printer(models.Model):

    name = models.CharField(max_length=255, verbose_name='Наименование принтера')
    api_key = models.CharField(max_length=32, verbose_name='Ключ доступа к API')
    check_type = models.CharField(max_length=16, verbose_name='Тип чека')
    point_id = models.IntegerField(verbose_name='Идентификатор точки')
