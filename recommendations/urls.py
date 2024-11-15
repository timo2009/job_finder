# recommendations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('model/train/', views.trigger_training, name='trigger_training'),
    path('model/', views.model_index, name='model'),

    path('', views.submit_profile, name='submit_profile'),
    path('impressum/', views.impressum, name='impressum'),
    path('get_recommendation', views.get_recommendation, name='get_recommendation'),
    path('get_recommendation', views.get_recommendation, name='get_recommendation'),
    path('save_feedback/', views.save_feedback, name='save_feedback'),

]
