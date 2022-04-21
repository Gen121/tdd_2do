import os
import time
from unittest import TestCase

from .tasks import TasksCRUD

APP_TOKEN_FILE = "token.json"
USER_TOKEN_FILE = "user_token.json"


class TaskListCRUD(TestCase):
    # Создаем объект TasksCRUD API c соответствующими параметрами

    def setUp(self) -> None:
        super().setUpClass()
        self.api = TasksCRUD()
        self.items = self.api.get_list_tasklists()
        tests_str = ['Task_List_from_Python', 'Changed_Task_List']
        for item in self.items:
            try:
                if item.get('title') in tests_str:
                    self.api.service.tasklists().delete(
                        tasklist=item.get('id')).execute()
            except Exception as e:
                print(e)
        time.sleep(0.5)

    def test_task_list_CRUD(self):
        # Получаем список СпискЗадач: List[< tasklist >]
        # В нем отсутствует 'Task List from Python'
        items = self.api.get_list_tasklists()
        self.assertNotIn('Task_List_from_Python',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>>')

        # создаем СпискЗадач: Create < tasklist >
        self.api.insert_tasklist()
        time.sleep(0.5)
        items = self.api.get_list_tasklists()
        self.assertIn('Task_List_from_Python',
                      [item['title'] for item in items],
                      '<<< Error: НЕ в списке >>>')

        # пробуем изменить созданный СпискЗадач: Read, Update < tasklist >
        self.api.update_task_list()
        time.sleep(0.5)
        items = self.api.get_list_tasklists()
        self.assertIn('Changed_Task_List',
                      [item['title'] for item in items],
                      '<<< Error: НЕ в списке >>>')
        # Убедимся что СпискаЗадач с прошлым названием нет в списке
        items = self.api.get_list_tasklists()
        self.assertNotIn('Task_List_from_Python',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>')

        # пробуем удалить созданный СпискЗадач: Delete < tasklist >
        self. api.delete_task_list()
        time.sleep(0.5)
        items = self.api.get_list_tasklists()
        self.assertNotIn('Changed_Task_List',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>')


class TaskCRUD(TestCase):
    # Создаем объект TasksCRUD API c соответствующими параметрами
    def setUp(self) -> None:
        super().setUpClass()
        self.api = TasksCRUD()
        self.items = self.api.get_list_task()
        tests_str = ['Task_Python', 'Changed_Task']
        for item in self.items:
            try:
                if item.get('title') in tests_str:
                    self.api.service.tasklists().delete(
                        tasklist=item.get('id')).execute()
            except Exception as e:
                print(e)
        time.sleep(0.5)

    def test_task_CRUD(self):
        # Получаем список Задач: List[< task >]
        # в нем отсутствует 'Task Python'
        items = self.api.get_list_task()
        self.assertNotIn('Task_Python',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>>')

        # Создаем Задачу: Create < task >
        self.api.insert_task()
        time.sleep(0.5)
        items = self.api.get_list_task()
        self.assertIn('Task_Python',
                      [item['title'] for item in items],
                      '<<< Error: НЕ в списке >>>')

        # Пробуем изменить созданную Задачу: Read, Update < taskl >
        self.api.update_task_title()
        time.sleep(0.5)
        items = self.api.get_list_task()
        self.assertIn('Changed_Task',
                      [item['title'] for item in items],
                      '<<< Error: НЕ в списке >>>')

        # Убедимся что Задачи с прошлым названием нет в списке
        items = self.api.get_list_task()
        self.assertNotIn('Task_Python',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>')

        # Пробуем удалить созданную Задачу: Delete < taskl >
        self. api.delete_task(title='Changed_Task')
        time.sleep(0.5)
        items = self.api.get_list_task()
        self.assertNotIn('Changed_Task',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>')
