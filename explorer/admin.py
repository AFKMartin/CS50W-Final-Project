from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(GameScore)
admin.site.register(Achievement)
admin.site.register(UserAchievement)