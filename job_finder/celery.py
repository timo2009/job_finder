from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Setze das Django Settings Modul für das Celery App
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_finder.settings')

app = Celery('job_finder')

# Lese die Konfiguration aus der Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Aktiviere die automatische Erkennung von Aufgaben in Django Apps
app.autodiscover_tasks()

# Optionale Konfigurationseinstellungen
app.conf.broker_url = 'redis://localhost:6379/0'  # Verbindung zur Redis-Instanz
app.conf.accept_content = ['json']  # Erlaubte Inhalte für Aufgaben
app.conf.task_serializer = 'json'  # Serializer für Aufgaben
app.conf.result_backend = 'redis://localhost:6379/0'  # Optional: Um Ergebnisse zu speichern
app.conf.broker_connection_retry_on_startup = True  # Um die Warnung zu beheben
app.conf.broker_transport_options = {
    'visibility_timeout': 3600,  # Optional: Sichtbarkeits-Timeout für Nachrichten
    'retry_policy': {
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
