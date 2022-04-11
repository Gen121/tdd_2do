from typing import Any
# from django.http import HttpResponse
from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):
    """Теcт домашней страницы"""

    def test_home_page_use_correct_template(self):
        """тест: домашняя страница использует правильный html шаблон"""
        response: Any = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):
    """Тест модели элемента списка"""

    def test_saving_and_retriving_items(self):
        # Зто - Интегрированный тест тк опирается на внешнюю систему – бд
        # Этот модульный тест в очень многословном стиле
        # Не рекомендуется писать так в реальной ситуации
        # В главе 15 мы этот тест перепишем, чтобы он стал намного короче
        """тест: сохранение и получение моделей списка"""
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (Ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (Ever) list item')
        self.assertEqual(first_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_item.list, list_)


class ListViewTest(TestCase):
    """тест представления списка"""

    def test_usess_list_template(self):
        """тест: используется шаблон списка"""
        list_ = List.objects.create()
        response: Any = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """тест: передается правильныйшаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response: Any = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        """тест: отображения списка элементов по URL"""
        correct_list = List.objects.create()

        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)

        other_list = List.objects.create()

        Item.objects.create(text='other_item 1', list=other_list)
        Item.objects.create(text='other_item 2', list=other_list)

        response: Any = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other_item 1')
        self.assertNotContains(response, 'other_item 2')
        # по сравнению со старым вариантом assertIn:
        # "self.assertIn('item 1', response.content.decode())" -
        # assertContains: сообщает - тест не проходит, тк новый
        # URL-адрес еще не существует, и возвращает код состояния 404:
        # "AssertionError: 404 != 200: Couldn't retrieve content: Response..."


class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можно сохранить POST запрос"""
        # TODO Вместо аннотации 'Any' изменить на требуемый
        # Код с душком: тест POST-запроса слишком длинный?
        ITEM_OBJECTS_COUNT: int = 1

        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), ITEM_OBJECTS_COUNT)
        new_item: Any = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после POST запроса на / """
        response: Any = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})
        new_list: Any = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        # assertRedirects эквивалентен двум следующим ассертам:
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/one-...

        # В книге предлагается исп. "/lists/один-единственный-список-в-мире/"
        # но это приводит к дополнительным проблемам, видимо, с кодировкаой


class NewItemTest(TestCase):
    """тест нового элемента списка"""
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можно сохранить POST запрос"""
        # TODO Вместо аннотации 'Any' изменить на требуемый
        # Код с душком: тест POST-запроса слишком длинный?
        ITEM_OBJECTS_COUNT: int = 1
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new list item for an existing list'})

        self.assertEqual(Item.objects.count(), ITEM_OBJECTS_COUNT)
        new_item: Any = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """тест: переадресует после POST запроса на / """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response: Any = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new list item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
        # assertRedirects эквивалентен двум следующим ассертам:
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/one-...

        # В книге предлагается исп. "/lists/один-единственный-список-в-мире/"
        # но это приводит к дополнительным проблемам, видимо, с кодировкаой