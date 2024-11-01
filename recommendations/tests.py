from django.test import TestCase
from .tasks import test_task  # Importiere deine Celery-Task

class TaskTest(TestCase):
    def test_my_task(self):
        result = test_task.delay()  # Starte die Celery-Task
        self.assertEqual(result.get(timeout=10), 'expected result')  # Überprüfe das Ergebnis
