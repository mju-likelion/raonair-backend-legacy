from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from . import models
from datetime import datetime

import base64
import os

# Create your views here.
def home(request) :
    return JsonResponse({"request": "home.html"})

# 검색결과 페이지
def search_play(request):
    return JsonResponse({"request": "searchPage.html"})

# 검색 결과 페이지, 더보기 클릭 (GET /api/search/:type)
def search_detail(request, type, start):
    keyword = request.GET.get("query", "")
    plays = models.Play.objects.filter(title__icontains=keyword)  # play 모든 결과 불러옴

    search_list = []  # 검색 결과들
    data_start = 0 # 앞으로 가져올 데이터의 시작점
    #print(request.resolver_match.url_name)
    #print(request.resolver_match.view_name)
    print(request.get_full_path())

    if start:
        next = request.get_full_path().split("&start")[0]
        + "&start"
        + "string(start+10)"
    else:
        next = request.get_full_path() + "&start=11"

    # 검색 결과가 0개 일 때
    if len(plays) == 0:
        return JsonResponse({
            "error": {
                "query": keyword,
                "type": type,
                "error_message": "검색 결과가 없습니다",
            }
        })

    for i in plays:
        new_play = ({
            "title": i.title,
            "poster": i.poster,
            "start_date": i.start_date,
            "end_date": i.end_date,
        })
        search_list.append(new_play)

    # 더보기를 눌러서 더 많은 공연을 조회했을 때
    return JsonResponse({
        "links": {
            "next": next
        },
        "data": {
            "query": keyword,
            "type": type,
            "search_results": search_list[data_start:data_start+10],
        },
    })

def troupe(request) :
    return JsonResponse({"request": "listpage.html"})

def play(request) :
    return JsonResponse({"request":"play.html"})

def signin(request) :
    return  JsonResponse({"request": "signin.html"})

def signup(request) :
    return  JsonResponse({"request": "signup.html"})

def password(request) :
    return  JsonResponse({"request": "find-password.html"})

def playlike(request) :
    return  JsonResponse({"request": "playlike.html"})

def troupelike(request) :
    return  JsonResponse({"request": "troupelike.html"})

def star(request) :
    return  JsonResponse({"request": "star.html"})

def comment(request) :
    return  JsonResponse({"request": "comment.html"})