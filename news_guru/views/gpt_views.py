from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from ..models import News, MEDIA_MAPPING
from django.core.paginator import Paginator  
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
import requests
from django.db.models import Min, Max
from django.views.generic import ListView
from openai import OpenAI
import json
from django.conf import settings


CARD_NEWS_API_KEY = settings.CARD_NEWS_API_KEY
BACKGROUND_KNOWLEDGE_API_KEY = settings.BACKGROUND_KNOWLEDGE_API_KEY
KEYWORDS_EXPLANATIONS_API_KEY = settings.KEYWORDS_EXPLANATIONS_API_KEY


def generate_card_news(request, id):
    news = get_object_or_404(News, pk=id)
    news_content = news.content
    
    # Initialize your OpenAI client
    client = OpenAI(api_key=CARD_NEWS_API_KEY)

    # Generate the prompt for DALL-E
    prompt = f"""Create a visual representation for the following news article, leaving space for text:
    {news_content}
    """

    # Call the OpenAI API to generate an image
    response = client.images.generate(
        model="dall-e-3",  # Make sure to use the correct model name
        prompt=prompt,
        size="1024x1024",
        n=1
    )

    # Extract the image URL from the response
    image_url = response.data[0].url

    # Return the image URL in a JsonResponse
    return JsonResponse({'image_url': image_url})


def get_background_knowledge(request, id):
    # Assuming you have a way to get the news content by its ID
    news = get_object_or_404(News, pk=id)
    news_content = news.content
    news_url = news.url
    client = OpenAI(api_key=BACKGROUND_KNOWLEDGE_API_KEY)

    response = client.chat.completions.create(
      model="gpt-4-0125-preview",
      temperature=0.2,
      messages=[
            {"role": "system", "content": "You are a helpful assistant for news readers."},
            {"role": "user", "content": f"""
             news article : {news_content}, url : {news_url}
             Use Browse with Bing : Based on the above news article, find a few previous news articles to help news readers understand the above news article. 
             Then, based on previous articles, Please provide the background knowledge of the above news article.
             Please make sure that the content of the above article is not included in the background knowledge as much as possible so that the previous background can be reflected.
             Finally, please print out 3 to 5 sentences in Korean.
             """},
            ]
    )

    background_knowledge = response.choices[0].message.content
    return JsonResponse({'background_knowledge': background_knowledge})


def get_keywords_and_explanations(request, id):
    # Assuming you have a way to get the news content by its ID
    news = get_object_or_404(News, pk=id)
    news_content = news.content
    client = OpenAI(api_key=KEYWORDS_EXPLANATIONS_API_KEY)
    
    response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      temperature=0.2,
      response_format={
          'type' : 'json_object'
      },
      messages=[
            {"role": "system", "content": "You are a helpful assistant for news readers designed to output JSON."},
            {"role": "user", "content": f"""Identify technical terms, new words, and hard foreign words from the following news article, and store the words each in a key in the form of JSON. 
             Provide explanations for the words IN KOREAN, and store the explanations each in a value in the form of JSON.
             news article : 
             국적 불문 최고 인기 메뉴는 ‘치킨’
            2위 ‘간장게장’, 중화권 여행객 사이 인기
            글로벌 K관광 플랫폼 ‘크리에이트립’이 작년 한 해 한국을 방문한 외국인 관광객들의 외식메뉴 거래 데이터를 바탕으로 국적별 외식메뉴 소비 트렌드를 21일 발표했다. 작년 한 해 국적 불문 가장 인기를 끈 메뉴는 ‘치킨’ 으로 전체 외식메뉴 중 거래건수 1 위를 기록한 것으로 나타났다. 2위는 간장게장이 차지했다.
            코로나19 발생 이전인 2019년과 비교한 결과 2023년 크리에이트립의 작년 외식메뉴 카테고리 거래건수는 약 11배, 거래액은 약 57배 증가했다.
            작년 한 해 한국 방문 외국인들이 가장 많이 찾은 메뉴는 ‘치킨’이었다. 전체 외식메뉴 중 거래건수 1 위를 기록했다. 크리에이트립은 “한국어가 유창하지 않아도 온라인 배달 주문으로 이용할 수 있고, 치킨 프랜차이즈 브랜드 교촌치킨에서 운영하는 ‘교촌필방’ 등 새로운 방식으로 치킨을 즐길 수 있는 오프라인 매장에도 많이 방문하고 있기 때문으로 보인다”고 설명했다.
            의외의 메뉴도 눈에 띈다. 바로 ‘간장게장’이다 . 간장게장은 치킨에 이어 거래건수 기준 전체 외식메뉴 중 2 위를 차지한 것으로 나타났다 . 특히 대만과 홍콩 등 중화권 여행객 사이에서 거래건수가 전체의 약 87%, 거래액은 전체의 약 89%로 큰 비중을 차지하고 있다. 크리에이트립을 이용한 대만인 여행객은 “기후가 더운 나라에서는 날것의 해산물을 안전하게 조리해 먹는 요리가 드물다”며 “간장게장의 맛 또한 많이 달거나 짜지 않아 입맛에 잘 맞는다”며 선호 이유를 밝혔다 .
            중화권 관광객 사이에서는 간장게장 외에도 고기구이와 분식 메뉴가 인기 있는 것으로 나타났다. 전체 고기구이 전문점 거래 데이터 중 중화권 관광객의 거래 건수는 약 77%, 거래액은 약 83% 의 비중을 기록하며 육류 요리 수요를 견인 중이다. 분식 또한 전체 수요의 약 60%를 차지하며 과반 이상을 차지했다.
            한식 중 간장게장, 고기구이 등이 인기가 많은 중화권과 달리 일본 관광객은 정갈한 한정식을 많이 찾았다. 일본은 전체 한정식 거래 건수 및 거래액의 약 80%를 기록하며 압도적인 소비층으로 자리 잡았다. 또한 전통 약과를 현대식으로 재해석한 디저트 매장이 인기를 끌며 전체 거래 규모의 약 57%를 차지했다 .
            서양권 및 싱가포르 여행객의 외식 메뉴 선호도는 아시아권 여행객과 다른 양상을 보였다. 해당 지역 여행객들이 선호한 음식 1위와 2위는 각각 치킨과 분식이었으나 유일하게 ‘빙수’가 상위 3위 안에 들었다. 빙수 외에도 토스트, 도넛 등 간식 메뉴가 상위권에 올랐다. 아시아권 관광객에게 인기 있는 간장게장, 찜닭, 고기구이 등 한식 메뉴보다 입맛에도 익숙하고 간단히 즐길 수 있는 디저트를 자주 찾는 것으로 분석된다.
             """},
            {"role": "assistant", "content": """
             {'거래 데이터' : '거래 내역이나 정보를 수집한 자료', 
             '소비 트렌드' : '사람들이 어떤 상품이나 서비스를 소비하는 경향', 
             '플랫폼' : '다양한 응용 프로그램이 구동될 수 있는 기반 기술 또는 서비스', 
             '거래액' : '상품이나 서비스의 거래에서 발생한 총 금액', 
             '크리에이트립' : '외국인을 대상으로 한국 여행과 관련된 관광 정보 및 예약 서비스를 제공하는 온라인 플랫폼', 
             'K관광' : '한국을 방문하는 관광'}
             """
            },
            {"role": "user", "content": f"""Identify technical terms, new words, and hard foreign words from the following news article, and store the words each in a key in the form of JSON. 
             Provide explanations for the words IN KOREAN, and store the explanations each in a value in the form of JSON.
             news article : {news_content}
             """},
            ]
    )
    
    keywords_explanation = json.loads(response.choices[0].message.content)
    return JsonResponse(keywords_explanation)