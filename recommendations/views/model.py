import joblib
import json
from ..models import PersonalityProfile, DreamJob, Skill, Interest, Fun
from ..tasks import train_model  # Importiere die train_model-Task
from django.contrib.admin.views.decorators import staff_member_required  # Importiere den Dekorator

from django.shortcuts import render, redirect
from django.contrib import messages
from celery.exceptions import OperationalError

@staff_member_required
def model_index(request):
    return render(request, 'model/index.html')
@staff_member_required  # Only for administrators
def trigger_training(request):
    if request.method == 'POST':
        try:
            result = train_model.delay()  # Asynchronous call of the function
            messages.success(request,
                             "Training has been successfully initiated! Result: " + str(result))  # Success message
        except OperationalError as e:
            messages.error(request, f"Celery Error: {str(e)}")  # Error message
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")  # General error message

        return redirect('trigger_training')  # Redirection to the same page

    # If the method is not POST, render the appropriate template
    return render(request, 'model/trigger_training.html')  # Replace 'your_template.html' with your template name

