from django.db import models


# Create your models here.
class News(models.Model):
    publish_date = models.DateField()
    press = models.IntegerField()
    category = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.TextField()
    thumbnail_url = models.TextField()
    
class SurveyResponse(models.Model):
    card_news_satisfaction = models.CharField(max_length=10)
    background_satisfaction = models.CharField(max_length=10)
    keywords_satisfaction = models.CharField(max_length=10)
    service_satisfaction = models.CharField(max_length=10)
    feedback = models.TextField()
    phone_num = models.CharField(max_length=20)

class CardNews(models.Model):
    news_id = models.IntegerField()
    card_news_url = models.TextField()
    satisfaction = models.BooleanField()

class BackGround(models.Model):
    news_id = models.IntegerField()
    background_text = models.TextField()
    satisfaction = models.BooleanField()
    
class KeyWords(models.Model):
    news_id = models.IntegerField()
    keywords_json = models.JSONField()
    satisfaction = models.BooleanField()
    
MEDIA_MAPPING = {
    32: "경향신문",
    5: "국민일보",
    20: "동아일보",
    21: "문화일보",
    81: "서울신문",
    22: "세계일보",
    23: "조선일보",
    25: "중앙일보",
    28: "한겨레",
    469: "한국일보"
    # Add more mappings as needed
}