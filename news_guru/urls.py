from django.urls import path
from .views import base_views, gpt_views

app_name = 'news_guru'

urlpatterns = [
    path('',
         base_views.home, name='home'),
    path('intro/',
         base_views.intro, name='intro'),
    path('survey/',
         base_views.survey, name='survey'),
    path('submit_survey/',
         base_views.submit_survey, name='submit_survey'),
    path('news/',
         base_views.index, name='index'),
    path('<int:id>/',
         base_views.detail, name='detail'),
    path('<int:id>/generate_card_news/', 
         gpt_views.generate_card_news, name='generate_card_news'),
    path('<int:id>/get_background_knowledge/', 
         gpt_views.get_background_knowledge, name='get_background_knowledge'),
    path('<int:id>/get_keywords_and_explanations/', 
         gpt_views.get_keywords_and_explanations, name='get_keywords_and_explanations')
]