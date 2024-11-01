# recommendations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_profile, name='submit_profile'),  # Benutzer-Trainingsansicht
    path('train/', views.trigger_training, name='trigger_training'),  # Admin-Trainingsansicht
    path('impressum/', views.impressum, name='impressum'),  # Benutzer-Trainingsansicht
    path('get_recommendation', views.get_recommendation, name='get_recommendation'),  # Modell-Nutzungsansicht
]
