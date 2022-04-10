from django.db import models


class Item(models.Model):
    """"Элемент списка"""
    text = models.CharField(max_length=255, default='<Узелок>')
    list = models.ForeignKey('List',
                             verbose_name='list',
                             on_delete=models.CASCADE,
                             default=None)


class List(models.Model):
    """Список элементов"""
    pass
