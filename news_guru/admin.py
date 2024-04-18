from django.contrib import admin

# Register your models here.
from .models import SurveyResponse, CardNews, BackGround, KeyWords 

admin.site.register(SurveyResponse)
admin.site.register(CardNews)
admin.site.register(BackGround)
admin.site.register(KeyWords)