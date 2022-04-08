from typing import Any

# from django.http import HttpResponse
from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    """Теcт домашней страницы"""

    def test_home_page_use_correct_template(self):
        """тест: домашняя страница использует правильный html шаблон
        """
        response: Any = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить POST запрос
        """
        # TODO Вместо аннотации 'Any' изменить на требуемый
        # Код с душком: тест POST-запроса слишком длинный?
        ITEM_OBJECTS_COUNT: int = 1
        response: Any = self.client.post(
            '/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), ITEM_OBJECTS_COUNT)

        new_item: Any = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

    def test_only_save_items_when_necessary(self):
        """тест: сохраняет элементы только когда нужно"""
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTesr(TestCase):
    """Тест модели элемента списка
    """

    def test_saving_and_retriving_items(self):
        # Зто - Интегрированный тест тк опирается на внешнюю систему – бд
        # Этот модульный тест в очень многословном стиле
        # Не рекомендуется писать так в реальной ситуации
        # В главе 15 мы этот тест перепишем, чтобы он стал намного короче
        """тест: сохранение и получение моделей списка"""
        first_item = Item()
        first_item.text = 'The first (Ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (Ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
