import joblib
import json
from .models import PersonalityProfile, DreamJob, Skill, Interest, Fun
from .tasks import train_model  # Importiere die train_model-Task
from django.contrib.admin.views.decorators import staff_member_required  # Importiere den Dekorator

from django.shortcuts import render, redirect
from django.contrib import messages
from celery.exceptions import OperationalError

@staff_member_required  # Only for administrators
def trigger_training(request):
    print("start")
    if request.method == 'POST':
        try:
            print("post")
            result = train_model.delay()  # Asynchronous call of the function
            print(result)
            messages.success(request, "Training has been successfully initiated!")  # Success message
        except OperationalError as e:
            messages.error(request, f"Celery Error: {str(e)}")  # Error message
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")  # General error message

        return redirect('trigger_training')  # Redirection to the same page

    # If the method is not POST, render the appropriate template
    return render(request, 'trigger_training.html')  # Replace 'your_template.html' with your template name

def submit_profile(request):
    if request.method == 'POST':
        # Formulardaten verarbeiten
        skills_names = request.POST.get('skills', '').split(',')  # Mehrere Fähigkeiten erhalten
        funs_names = request.POST.get('funs', '').split(',')  # Mehrere Spaßmachsachen erhalten
        interests_names = request.POST.get('interests', '').split(',')  # Mehrere Interessen erhalten
        job_title = request.POST.get('job_title')
        satisfaction = int(request.POST.get('satisfaction'))

        # Neues Profil speichern
        profile = PersonalityProfile.objects.create()

        # Füge die gewählten Fähigkeiten hinzu oder erstelle sie
        for skill_name in skills_names:
            skill_name = skill_name.strip()  # Leerzeichen entfernen
            if skill_name:  # Nur hinzufügen, wenn der Name nicht leer ist
                skill, created = Skill.objects.get_or_create(name=skill_name)
                profile.skills.add(skill)

        # Füge die gewählten Interessen hinzu oder erstelle sie
        for interest_name in interests_names:
            interest_name = interest_name.strip()  # Leerzeichen entfernen
            if interest_name:
                interest, created = Interest.objects.get_or_create(name=interest_name)
                profile.interests.add(interest)

        # Füge die gewählten Funs hinzu oder erstelle sie
        for fun_name in funs_names:
            fun_name = fun_name.strip()  # Leerzeichen entfernen
            if fun_name:
                fun, created = Fun.objects.get_or_create(name=fun_name)
                profile.funs.add(fun)

        # Zuordnung des Jobs
        DreamJob.objects.create(profile=profile, job_title=job_title, satisfaction=satisfaction)

        return render(request, 'submit_profile_result.html')

    # Wenn die Anfrage nicht POST ist, alle verfügbaren Fähigkeiten und Interessen abrufen
    skills = list(Skill.objects.values_list('name', flat=True))  # All skills
    interests = list(Interest.objects.values_list('name', flat=True))  # All interests
    funs = list(Fun.objects.values_list('name', flat=True))  # All fun activities

    return render(request, 'submit_profile.html', {
        'skills': json.dumps(skills),
        'interests': json.dumps(interests),
        'funs': json.dumps(funs)
    })


def get_recommendation(request):
    if request.method == 'POST':
        # Eingabedaten des Benutzers abrufen
        skills_names = request.POST.getlist('skills')  # Mehrere Fähigkeiten erhalten
        interests_names = request.POST.getlist('interests')  # Mehrere Interessen erhalten
        funs_names = request.POST.getlist('funs')  # Mehrere Fun-Aktivitäten erhalten

        # KI-Modell und Vektorisierer laden
        model = joblib.load('model.joblib')
        vectorizer = joblib.load('vectorizer.joblib')  # Vektorisierer laden

        # Profildaten vorbereiten
        # Kombiniere alle Texte in einem String
        profile_data = ' '.join(skills_names + interests_names + funs_names)  # Texte kombinieren

        # Vektorisierung der Profildaten
        profile_vector = vectorizer.transform([profile_data])  # Transformiere den Text in ein Vektorformat

        # Job-Vorschlag generieren
        recommended_job = model.predict(profile_vector)[0]

        # Zufriedenheit überprüfen und bei positiver Rückmeldung Profil zum Training verwenden
        satisfaction = request.POST.get('satisfaction')
        if satisfaction and int(satisfaction) >= 8:
            # Profil speichern für Training
            profile = PersonalityProfile.objects.create(use_for_training=True)

            # Füge die gewählten Fähigkeiten hinzu oder erstelle sie
            for skill_name in skills_names:
                skill, created = Skill.objects.get_or_create(name=skill_name)  # Suche oder erstelle die Fähigkeit
                profile.skills.add(skill)  # Füge die Fähigkeit zum Profil hinzu

            # Füge die gewählten Interessen hinzu oder erstelle sie
            for interest_name in interests_names:
                interest, created = Interest.objects.get_or_create(name=interest_name)  # Suche oder erstelle das Interesse
                profile.interests.add(interest)  # Füge das Interesse zum Profil hinzu

            # Füge die gewählten Funs hinzu oder erstelle sie
            for fun_name in funs_names:
                fun, created = Fun.objects.get_or_create(name=fun_name)  # Suche oder erstelle das Fun
                profile.funs.add(fun)  # Füge das Fun zum Profil hinzu

            # Speichere den empfohlenen Job
            DreamJob.objects.create(profile=profile, job_title=recommended_job, satisfaction=int(satisfaction))

        return render(request, 'get_recommendation_result.html', {
            'recommended_job': recommended_job,
        })

    # Wenn die Anfrage nicht POST ist, alle verfügbaren Fähigkeiten, Interessen und Fun-Aktivitäten abrufen
    skills = list(Skill.objects.values_list('name', flat=True))  # All skills
    interests = list(Interest.objects.values_list('name', flat=True))  # All interests
    funs = list(Fun.objects.values_list('name', flat=True))  # All fun activities

    return render(request, 'get_recommendation.html', {
        'skills': json.dumps(skills),
        'interests': json.dumps(interests),
        'funs': json.dumps(funs)
    })