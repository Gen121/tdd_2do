import os
import time
from unittest import TestCase

from .tasks import TasksCRUD

APP_TOKEN_FILE = "token.json"
USER_TOKEN_FILE = "user_token.json"


class TaskListCRUDTestCase(TestCase):
    # Создаем объект TasksCRUD API c соответствующими параметрами

    def setUp(self) -> None:
        super().setUpClass()
        self.api = TasksCRUD()
        self.items = self.api.get_list_tasklists()
        for item in self.items:
            try:
                if item.get('title') == 'Task List from Python':
                    self.api.service.tasklists().delete(
                        tasklist=item.get('id')).execute()
            except Exception as e:
                print(e)
        time.sleep(0.5)

    def test_taskList_CRUD(self):
        # Получаем список СпискЗадач: List[< tasklist >]
        # В нем отсутствует 'Task List from Python'
        items = self.api.get_list_tasklists()
        self.assertNotIn('Task List from Python',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>>')

        # создаем СпискЗадач: Create < tasklist >
        self.api.insert_task_list()
        time.sleep(0.5)
        items = self.api.get_list_tasklists()
        self.assertIn('Task List from Python',
                      [item['title'] for item in items],
                      '<<< Error: НЕ в списке >>>')

        # пробуем изменить созданный СпискЗадач: Read, Update < tasklist >
        self.api.update_task_list()
        time.sleep(0.5)
        items = self.api.get_list_tasklists()
        self.assertIn('Changed Task List',
                      [item['title'] for item in items],
                      '<<< Error: НЕ в списке >>>')
        # Убедимся что СпискаЗадач с прошлым названием нет в списке
        items = self.api.get_list_tasklists()
        self.assertNotIn('Task List from Python',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>')

        # пробуем удалить созданный СпискЗадач: Delete < tasklist >
        self. api.delete_task_list()
        time.sleep(0.5)
        items = self.api.get_list_tasklists()
        self.assertNotIn('Changed Task List',
                         [item['title'] for item in items],
                         '<<< Error: В СПИСКЕ >>')
