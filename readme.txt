Start AI:
celery -A job_finder worker --loglevel=INFO
(venv)
sudo systemctl start redis
sudo systemctl status redis
(lokal)

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
                interest, created = Interest.objects.get_or_create(
                    name=interest_name)  # Suche oder erstelle das Interesse
                profile.interests.add(interest)  # Füge das Interesse zum Profil hinzu

            # Füge die gewählten Funs hinzu oder erstelle sie
            for fun_name in funs_names:
                fun, created = Fun.objects.get_or_create(name=fun_name)  # Suche oder erstelle das Fun
                profile.funs.add(fun)  # Füge das Fun zum Profil hinzu

            # Speichere den empfohlenen Job
            DreamJob.objects.create(profile=profile, job_title=recommended_job, satisfaction=int(satisfaction))