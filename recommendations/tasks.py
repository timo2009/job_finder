# tasks.py
from datetime import datetime, timedelta
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from job_finder.celery import app
import pytz
from .models import PersonalityProfile, DreamJob


@app.task
def test_task():
    return "Task completed!"

@app.task
def train_model():
    # Daten laden
    profiles = PersonalityProfile.objects.filter(use_for_training=True)
    jobs = DreamJob.objects.filter(profile__in=profiles)

    if not profiles.exists() or not jobs.exists():
        return "Nicht genügend freigegebene Daten für Training."

    # Daten und Labels initialisieren
    data, labels, weights = [], [], []

    # Aktuelle Zeit in UTC
    now_utc = datetime.now(pytz.utc)

    # Setze die Zeitzone für den aktuellen Zeitstempel
    recent_date_threshold = now_utc - timedelta(days=180)  # Die letzten 6 Monate

    for job in jobs:
        profile = job.profile
        # Bereite Textdaten vor
        skills = list(profile.skills.values_list('name', flat=True))
        interests = list(profile.interests.values_list('name', flat=True))
        funs = list(profile.funs.values_list('name', flat=True))

        profile_data = ' '.join(skills + interests + funs)
        data.append(profile_data)
        labels.append(job.job_title)

        # Gewichtung basierend auf Zufriedenheit und Alter
        satisfaction_weight = (job.satisfaction / 10)
        is_recent = job.date_created >= recent_date_threshold
        age_factor = 1 if is_recent else 0.5  # Reduziere Gewichtung bei älteren Daten
        weights.append(satisfaction_weight * age_factor)

    # Vektorisierung
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data)
    y = labels

    # Aufteilen der Daten
    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        X, y, weights, test_size=0.2, random_state=42)

    try:
        # Modelltraining mit Gewichtung
        model = RandomForestClassifier()
        model.fit(X_train, y_train, sample_weight=w_train)

        # Speichere Modell und Vektorisierer
        joblib.dump(model, 'model.joblib')
        joblib.dump(vectorizer, 'vectorizer.joblib')

        return "Training erfolgreich abgeschlossen!"
    except Exception as e:
        print(f"Fehler beim Trainieren des Modells: {e}")
        return "Fehler beim Trainieren des Modells."
