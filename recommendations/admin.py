# recommendations/admin.py

from django.contrib import admin
from .models import Skill, Interest, PersonalityProfile, DreamJob, Fun

admin.site.register(Skill)
admin.site.register(Interest)
admin.site.register(Fun)
admin.site.register(DreamJob)
admin.site.register(PersonalityProfile)
