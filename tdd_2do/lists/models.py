from django.db import models


class Item(models.Model):
    """"Элемент списка"""
    text = models.CharField(max_length=255, default='<Узелок>')
