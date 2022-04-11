from typing import Any, Dict
from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    """домашняя страница"""
    context: Dict[str, Any] = {'new_item_text': ''}
    context['items'] = Item.objects.all()
    return render(request, 'home.html')


def view_list(request,  list_id):
    """Представление списка"""
    context: Dict[str, Any] = {}
    list_ = List.objects.get(id=list_id)
    context['items'] = Item.objects.filter(list=list_)
    context['list'] = list_
    return render(request, 'list.html', context=context)


def new_list(request):
    """новый список"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """Новый пункт списка"""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/lists/{list_.id}/')
