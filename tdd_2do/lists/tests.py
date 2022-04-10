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
        response: Any = self.client.get('/lists/one-single-list-in-the-world/')

        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_list_items(self):
        """тест: отображения списка элементов по URL"""
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/one-single-list-in-the-world/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        # по сравнению со старым вариантом assertIn:
        # "self.assertIn('item 1', response.content.decode())" -
        # assertContains: сообщает - тест не проходит, тк новый
        # URL-адрес еще не существует, и возвращает код состояния 404:
        # "AssertionError: 404 != 200: Couldn't retrieve content: Response..."


class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить POST запрос"""
        # TODO Вместо аннотации 'Any' изменить на требуемый
        # Код с душком: тест POST-запроса слишком длинный?
        ITEM_OBJECTS_COUNT: int = 1

        self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), ITEM_OBJECTS_COUNT)
        new_item: Any = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после POST запроса на / """
        response: Any = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})

        self.assertRedirects(response, '/lists/one-single-list-in-the-world/')
        # assertRedirects эквивалентен двум следующим ассертам:
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/one-...

        # В книге предлагается исп. "/lists/один-единственный-список-в-мире/"
        # но это приводит к дополнительным проблемам, видимо, с кодировкаой
