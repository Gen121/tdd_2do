from typing import Dict
from django.shortcuts import render
from lists.models import Item


def home_page(request):
    """домашняя страница"""
    context: Dict[str, str] = {'new_item_text': ''}
    if request.method == 'POST':
        context = {'new_item_text': request.POST.get('item_text', '')}
        Item.objects.create(text=context['new_item_text'])
    return render(request, 'home.html', context=context)
