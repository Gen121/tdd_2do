from typing import Dict
from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):
    """домашняя страница"""
    context: Dict[str, str] = {'new_item_text': ''}
    if request.method == 'POST':
        context['new_item_text'] = request.POST.get('item_text', '')
        item = Item.objects.create(text=context['new_item_text'])
        context['new_item_text'] = item.text
        return redirect('/')
    return render(request, 'home.html', context=context)
