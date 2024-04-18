from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import News, CardNews, BackGround, KeyWords, MEDIA_MAPPING
from django.core.paginator import Paginator  
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Min, Max
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

@require_POST
@csrf_protect
def cardnews_survey(request):
    satisfaction = request.POST.get('satisfaction')
    news_id = request.POST.get('news_id')
    card_news_url = request.POST.get('card_news_url')

    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    cardnews_response = CardNews(
        satisfaction=satisfaction,
        news_id=news_id,
        card_news_url=card_news_url
    )
    cardnews_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 응답으로 JavaScript를 전송하여 창을 닫습니다.
    response = HttpResponse('<script>alert("감사합니다! 귀하의 의견이 성공적으로 제출되었습니다."); window.close();</script>')
    return response


@require_POST
@csrf_protect
def background_survey(request):
    satisfaction = request.POST.get('satisfaction')
    news_id = request.POST.get('news_id')
    background_text = request.POST.get('background_text')
    
    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    background_response = BackGround(
        satisfaction=satisfaction,
        news_id=news_id,
        background_text=background_text
    )
    background_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 응답으로 JavaScript를 전송하여 창을 닫습니다.
    response = HttpResponse('<script>alert("감사합니다! 귀하의 의견이 성공적으로 제출되었습니다."); window.close();</script>')
    return response


@require_POST
@csrf_protect
def keywords_survey(request):
    satisfaction = request.POST.get('satisfaction')
    news_id = request.POST.get('news_id')
    keywords_json = request.POST.get('keywords_json')
    
    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    keywords_response = KeyWords(
        satisfaction=satisfaction,
        news_id=news_id,
        keywords_json=keywords_json
    )
    keywords_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 응답으로 JavaScript를 전송하여 창을 닫습니다.
    response = HttpResponse('<script>alert("감사합니다! 귀하의 의견이 성공적으로 제출되었습니다."); window.close();</script>')
    return response