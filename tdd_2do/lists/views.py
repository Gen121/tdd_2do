from typing import Any, Dict
from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):
    """домашняя страница"""
    # context: Dict[str, Any] = {'new_item_text': ''}
    context = {}
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect('/')
    context['items'] = Item.objects.all()
    return render(request, 'home.html', context=context)
