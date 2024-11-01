# recommendations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('train/', views.trigger_training, name='trigger_training'),  # Admin-Trainingsansicht
    path('submit_profile/', views.submit_profile, name='submit_profile'),  # Benutzer-Trainingsansicht
    path('', views.get_recommendation, name='get_recommendation'),  # Modell-Nutzungsansicht
]
