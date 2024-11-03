from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Fun(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PersonalityProfile(models.Model):
    skills = models.ManyToManyField(Skill)  # Many-to-Many-Beziehung zu Fähigkeiten
    interests = models.ManyToManyField(Interest)  # Many-to-Many-Beziehung zu Interessen
    funs = models.ManyToManyField(Fun)  # Many-to-Many-Beziehung zu Interessen
    use_for_training = models.BooleanField(default=True)

    def __str__(self):
        return f"Fähigkeiten: {[skill.name for skill in self.skills.all()]}, Interessen: {[interest.name for interest in self.interests.all()]}, Was mir Spaß macht: {[fun.name for fun in self.funs.all()]}"


class DreamJob(models.Model):
    profile = models.ForeignKey(PersonalityProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    satisfaction = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job: {self.job_title}, Zufriedenheit: {self.satisfaction}"
