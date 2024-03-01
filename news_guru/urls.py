from django.urls import path
from .views import base_views, gpt_views

app_name = 'news_guru'

urlpatterns = [
    # base_views.py
    path('',
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