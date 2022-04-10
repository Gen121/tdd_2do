from typing import Any, Dict
from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):
    """домашняя страница"""
    context: Dict[str, Any] = {'new_item_text': ''}
    context['items'] = Item.objects.all()
    return render(request, 'home.html')


def view_list(request):
    """Представление списка"""
    context: Dict[str, Any] = {}
    context['items'] = Item.objects.all()
    return render(request, 'list.html', context=context)


def new_list(request):
    """новый список"""
    Item.objects.create(text=request.POST.get('item_text'))
    return redirect('/lists/one-single-list-in-the-world/')
