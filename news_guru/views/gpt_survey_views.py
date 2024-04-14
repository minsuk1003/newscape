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

@require_POST
@csrf_protect
def cardnews_survey(request):
    satisfaction = request.POST.get('satisfaction')
    
    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    cardnews_response = CardNews(
        satisfaction=satisfaction
    )
    cardnews_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 설문조사 제출 후 사용자를 감사 페이지 또는 홈페이지로 리디렉션할 수 있습니다.
    return redirect('../news_detail')


@require_POST
@csrf_protect
def background_survey(request):
    satisfaction = request.POST.get('satisfaction')
    
    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    background_response = CardNews(
        satisfaction=satisfaction
    )
    background_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 설문조사 제출 후 사용자를 감사 페이지 또는 홈페이지로 리디렉션할 수 있습니다.
    return redirect('../survey')


@require_POST
@csrf_protect
def keywords_survey(request):
    satisfaction = request.POST.get('satisfaction')
    
    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    keywords_response = CardNews(
        satisfaction=satisfaction
    )
    keywords_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 설문조사 제출 후 사용자를 감사 페이지 또는 홈페이지로 리디렉션할 수 있습니다.
    return redirect('../survey')