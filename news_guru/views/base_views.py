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

def index(request):
    news_list = News.objects.order_by('-publish_date')
    
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
