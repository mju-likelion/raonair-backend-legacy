from django.http import JsonResponse
from django.shortcuts import render
from . import models

import base64
import os

# Create your views here.
def home(request) :
    return JsonResponse({"request": "home.html"})

# 검색결과 페이지
def search_play(request):
    return JsonResponse({"request": "searchPage.html"})

# 검색 결과 페이지, 더보기 클릭 (GET /api/search/<str:type>)
def search_detail(request, type):
    keyword = request.GET.get("query", "")
    loc = request.GET.get("location", "")

    filter_keyword = models.Play.objects.filter(title__icontains=keyword)  # 검색어에 포함되는 play를 받아옴
    plays = filter_keyword.filter(theater__location__icontains=loc)

    search_list = []  # 검색 결과들

    # 검색 결과가 0 일 때
    if len(plays) == 0:
        return JsonResponse({
            "error": {
                "query": keyword,
                "type": type,
                "error_message": "검색 결과가 없습니다",
            }
        })

    # start 데이터가 있는 경우와 없는 경우
    if request.GET.get("start", ""):
        start = int(request.GET.get("start", ""))
        next = request.get_full_path().split("&start=")[0] \
                + "&start=" \
                + str(start + 10)
    else:
        start = 0
        next = request.get_full_path() + "&start=11"

    for i in plays:
        stars = models.Star.objects.filter(play=i.id)
        likes = models.Like.objects.filter(play=i.id).count()

        # 평균 별점 구하기
        star_sum = 0
        for each_star in stars:
            star_sum += each_star.star
        star_avg = star_sum / len(stars) / 2

        new_play = ({
            "title": i.title,
            "poster": i.poster,
            "start_date": i.start_date,
            "end_date": i.end_date,
            'star_avg': star_avg,
            "likes": likes,
            "location": i.theater.location,
        })
        search_list.append(new_play)

    # 검색결과가 0이 아닐 때
    return JsonResponse({
        "links": {
            "next": next
        },
        "data": {
            "query": keyword,
            "type": type,
            "search_results": search_list[start:start+10],
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