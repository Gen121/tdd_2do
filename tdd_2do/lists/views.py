from django.shortcuts import render
from lists.models import Item


def home_page(request):
    """домашняя страница"""
    context = {'new_item_text': request.POST.get('item_text', '')}
    item = Item()
    item.text = context['new_item_text']
    item.save()
    context['new_item_text'] = item.text
    return render(request, 'home.html', context=context)
