from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import News, SurveyResponse, MEDIA_MAPPING
from django.core.paginator import Paginator  
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
import requests
from django.db.models import Min, Max
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib import messages  
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'news_guru/home.html')

def intro(request):
    return render(request, 'news_guru/intro.html')

def survey(request):
    return render(request, 'news_guru/survey.html')

@require_POST
@csrf_protect
def submit_survey(request):
    card_news_satisfaction = request.POST.get('cardnewsLevel')
    background_satisfaction = request.POST.get('backgroundLevel')
    keywords_satisfaction = request.POST.get('keywordsLevel')
    service_satisfaction = request.POST.get('serviceLevel')
    feedback = request.POST.get('feedback')
    phone_num = request.POST.get('phoneNum')
    

    # 새 설문조사 응답 객체를 생성하고 데이터베이스에 저장합니다.
    survey_response = SurveyResponse(
        card_news_satisfaction=card_news_satisfaction,
        background_satisfaction=background_satisfaction,
        keywords_satisfaction=keywords_satisfaction,
        service_satisfaction=service_satisfaction,
        feedback=feedback,
        phone_num=phone_num
    )
    survey_response.save()
    
    # 사용자에게 감사 메시지를 전달합니다.
    messages.success(request, '감사합니다! 귀하의 의견이 성공적으로 제출되었습니다.')
    
    # 설문조사 제출 후 사용자를 감사 페이지 또는 홈페이지로 리디렉션할 수 있습니다.
    return redirect('../survey')


def index(request):
    order_by = request.GET.get('order_by', 'latest')
    
    if order_by == 'latest':
        news_list = News.objects.order_by('title', '-publish_date')
    else:  # 오래된 순
        news_list = News.objects.order_by('title', 'publish_date')
    
    # 중복 제거 추가 - title 기준
    news_list = news_list.distinct('title')
    
    # 페이지, 키워드 필터링 조건
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    
    # 필터링 조건 받기
    publish_date = request.GET.get('publish_date')
    categories = request.GET.getlist('category')
    presses = request.GET.getlist('press')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # 날짜 필터링
    if start_date and end_date:
        news_list = news_list.filter(publish_date__range=[start_date, end_date])
    elif start_date:
        news_list = news_list.filter(publish_date__gte=start_date)
    elif end_date:
        news_list = news_list.filter(publish_date__lte=end_date)
    
    # 카테고리 필터링
    if categories:
        news_list = news_list.filter(category__in=categories)

    # 언론사 필터링
    if presses:
        news_list = news_list.filter(press__in=presses)

    # 제목 검색어 필터링
    if kw:
        news_list = news_list.filter(title__icontains=kw)
    
    
    paginator = Paginator(news_list, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)
    
    # 카테고리 목록 조회
    category_list = News.objects.values('category').annotate(count=Count('category')).order_by('category')
    
    # 언론사 목록은 MEDIA_MAPPING에서 가져옴
    press_list = sorted(MEDIA_MAPPING.items(), key=lambda x: x[1])  # 코드 기준 정렬

    # Fetch the earliest and latest publish_date values from News items
    date_range = News.objects.aggregate(
        earliest_date=Min('publish_date'),
        latest_date=Max('publish_date')
    )
    
    context = {
        'news_list': page_obj, 'page': page, 'kw': kw,
        'publish_date': publish_date, 'start_date': start_date, 'end_date': end_date,
        'categories' : categories, 'presses': presses,
        'category_list' : category_list, 'press_list': press_list,
        'earliest_date': date_range['earliest_date'],
        'latest_date': date_range['latest_date']
    }
    
    return render(request, 'news_guru/news_list.html', context)

def detail(request, id):
    news = get_object_or_404(News, pk=id)
    context = {'news': news}
    return render(request, 'news_guru/news_detail.html', context)
