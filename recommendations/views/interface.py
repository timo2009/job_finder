import joblib
import json
from ..models import PersonalityProfile, DreamJob, Skill, Interest, Fun
from django.shortcuts import render, redirect
from django.contrib import messages


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

        return render(request, 'interface/submit_profile_result.html')

    # Wenn die Anfrage nicht POST ist, alle verfügbaren Fähigkeiten und Interessen abrufen
    skills = list(Skill.objects.values_list('name', flat=True))  # All skills
    interests = list(Interest.objects.values_list('name', flat=True))  # All interests
    funs = list(Fun.objects.values_list('name', flat=True))  # All fun activities
    jobs = list(set(DreamJob.objects.values_list('job_title', flat=True)))  # Alle Titel sind einzigartig

    return render(request, 'interface/submit_profile.html', {
        'skills': json.dumps(skills),
        'interests': json.dumps(interests),
        'funs': json.dumps(funs),
        'jobs': json.dumps(jobs)
    })


def get_recommendation(request):
    if request.method == 'POST':
        # Eingabedaten des Benutzers abrufen
        skills_names = request.POST.getlist('skills')
        interests_names = request.POST.getlist('interests')
        funs_names = request.POST.getlist('funs')

        # KI-Modell und Vektorisierer laden
        model = joblib.load('model.joblib')
        vectorizer = joblib.load('vectorizer.joblib')

        # Profildaten vorbereiten
        profile_data = ', '.join(skills_names) + ';' + ', '.join(interests_names) + ';' + ', '.join(funs_names)

        # Vektorisierung der Profildaten
        profile_vector = vectorizer.transform([profile_data])

        # Job-Vorschlag generieren
        recommended_job = model.predict(profile_vector)[0]

        # Empfehlung und Daten im Template anzeigen
        return render(request, 'interface/get_recommendation_result.html', {
            'recommended_job': recommended_job,
            'skills_names': skills_names,
            'interests_names': interests_names,
            'funs_names': funs_names,
        })

    # Wenn die Anfrage nicht POST ist, verfügbare Optionen abrufen
    skills = list(Skill.objects.values_list('name', flat=True))
    interests = list(Interest.objects.values_list('name', flat=True))
    funs = list(Fun.objects.values_list('name', flat=True))

    return render(request, 'interface/get_recommendation.html', {
        'skills': json.dumps(skills),
        'interests': json.dumps(interests),
        'funs': json.dumps(funs),
    })

def save_feedback(request):
    if request.method == 'POST':
        # Daten aus dem Feedback-Formular abrufen
        recommended_job = request.POST.get('recommended_job')
        satisfaction = request.POST.get('satisfaction')
        skills_names = request.POST.getlist('skills')
        interests_names = request.POST.getlist('interests')
        funs_names = request.POST.getlist('funs')

        print(satisfaction)

        if satisfaction and int(satisfaction) > 7:
            # Neues Profil für das Training erstellen
            profile = PersonalityProfile.objects.create(use_for_training=True)

            # Gewählte Fähigkeiten, Interessen und Funs speichern
            for skill_name in skills_names:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                profile.skills.add(skill)

            for interest_name in interests_names:
                interest, _ = Interest.objects.get_or_create(name=interest_name)
                profile.interests.add(interest)

            for fun_name in funs_names:
                fun, _ = Fun.objects.get_or_create(name=fun_name)
                profile.funs.add(fun)

            # Job und Zufriedenheit speichern
            DreamJob.objects.create(profile=profile, job_title=recommended_job, satisfaction=int(satisfaction))

        return render(request, 'interface/get_recommendation_result.html', {
            'message': 'Vielen Dank für Ihr Feedback!',
            'recommended_job': recommended_job
        })


    return render(request, 'interface/get_recommendation_result.html', {
        'message': 'Ungültige Anfrage. Bitte versuchen Sie es erneut.'
    })


def impressum(request):
    return render(request, 'interface/impressum.html', {})
